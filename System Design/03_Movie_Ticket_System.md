# 🎬 System Design: Movie Ticket Booking System (Like BookMyShow)

> **Level:** Beginner-Friendly | **Format:** What → Why → How → Impact
> **Stack:** Next.js + Node.js + MySQL + MongoDB (Polyglot) + Redis + CDN

---

## 📌 Table of Contents

1. [Requirements](#1-requirements)
2. [Scale & Constraints](#2-scale--constraints)
3. [Budget & Costing](#3-budget--costing)
4. [High Level Design (HLD)](#4-high-level-design-hld)
5. [Low Level Design (LLD)](#5-low-level-design-lld)
6. [Scalability Design](#6-scalability-design)
7. [Reliability & Fault Tolerance](#7-reliability--fault-tolerance)
8. [Flexibility & Extensibility](#8-flexibility--extensibility)
9. [Dev-Friendly Practices](#9-dev-friendly-practices)
10. [Final Notes (Beginner Friendly)](#10-final-notes-beginner-friendly)
11. [Scenario-Based Q&A](#11-scenario-based-qa)

---

## 1. REQUIREMENTS

### 🧠 Think of it like this:
> Imagine you're building a **digital version of a movie theatre counter**.
> People come, choose a movie, pick seats, pay, and get a ticket.
> Now scale that counter to serve **500 million people** across the country. That's the challenge!

---

### ✅ Functional Requirements (FR)
> **What the system MUST do** — these are the core features users expect.

| Feature | Description | Real-World Example |
|---|---|---|
| User Registration & Login | Users can sign up and log in | Like logging into Netflix |
| Browse Movies | See now-showing, upcoming movies | Like browsing a movie catalogue |
| Search & Filter | Search by movie, city, date, language | "Show me Hindi movies in Mumbai today" |
| View Theatre & Seats | See available theatres + seat map | Like picking an airplane seat |
| Select Seats | Pick 1 or more seats | Hold a seat for 10 minutes while paying |
| Make Payment | Pay via UPI, card, wallet | Like paying on Amazon |
| Get Booking Confirmation | Receive ticket via email/SMS | QR code on your phone |
| View Booking History | See past bookings | "Show me my last 3 bookings" |
| Admin Panel | Theatres can add shows, movies, pricing | Cinema owner adding new showtimes |
| Cancellation & Refund | Cancel ticket and get money back | Cancel within 1 hour for full refund |

---

### ⚙️ Non-Functional Requirements (NFR)
> **How well the system should work** — think of these as the "quality standards".

| Requirement | What It Means | Real-World Analogy |
|---|---|---|
| **Availability** | System must be up 99.99% of time | A cinema counter that never closes |
| **Low Latency** | Pages load fast (under 200ms) | Google search feels instant |
| **Consistency** | Same seat should NOT be booked twice | Two people cannot sit in seat A5 |
| **Scalability** | Handle 10x traffic on release of big movies | Avengers release day crowd |
| **Security** | Protect payment & user data | Your UPI PIN is safe |
| **Durability** | Bookings must never be lost | Ticket receipt stays forever |

> 💡 **Key NFR to remember:** The #1 challenge is **seat consistency** — when 1000 users try to book seat A5 at once, only ONE should succeed.

---

## 2. SCALE & CONSTRAINTS

### 🧠 Think of it like this:
> Start with a **small tea stall** that serves 10 people per day.
> Now imagine it becomes **McDonald's** serving millions. The infra needs to grow accordingly.

---

### 📊 Traffic Estimation

#### Assumptions:
- **500 million registered users**
- **5 million active users per day (DAU)**
- **1 million bookings per day**
- **Peak hours:** 6 PM – 11 PM (5 hours), accounts for 60% of traffic

```
Daily Bookings     = 1,000,000 / day
Bookings per hour  = 1,000,000 / 24 ≈ 42,000 / hour (normal)
Peak hour booking  = 42,000 × 3 = ~125,000 / hour = ~35 bookings/sec

Reads (browsing)   = 10× writes = 350 reads/sec (normal)
Peak reads         = 3500 reads/sec (big movie release)
```

---

### 💾 Storage Estimation

```
User table         = 500M users × 1 KB per user     = 500 GB
Bookings           = 1M/day × 2 KB × 365 days       = 730 GB/year
Movies metadata    = 10,000 movies × 50 KB           = 500 MB
Show schedules     = 100,000 shows/day × 2 KB        = 200 MB/day
Seat maps          = 10,000 theatres × 5 KB          = 50 MB
Total (Year 1)     ≈ ~1.5 TB of structured data

Media (Posters, Trailers) = 10,000 movies × 10 MB   = 100 GB (stored on CDN)
```

---

### 📈 Peak vs Normal Load

```
                Normal Day          Big Movie Release Day
                ──────────          ─────────────────────
Traffic         35 req/sec          500+ req/sec
Seat Conflicts  Low                 VERY HIGH (1000s compete)
DB Load         Normal              Heavy (READ + WRITE surge)
Cache Hit Rate  80%                 95%+ (cache everything!)
Server Count    5–10 servers        50–100 servers (auto-scale)
```

---

## 3. BUDGET & COSTING

### 🧠 Think of it like this:
> A startup rents a small shop. A mid-size business takes an office floor. A big company owns the building.
> Similarly, cloud infra scales with your needs — and so does your bill.

---

### 💰 Startup Phase (0 – 100K users)

| Component | Choice | Rough Cost |
|---|---|---|
| Frontend hosting | Vercel (free tier for Next.js) | Free–$20/month |
| Backend | Single Node.js server on EC2/Railway | $20–$50/month |
| Database | MongoDB Atlas free tier → M10 | Free → $57/month |
| Cache | Redis Cloud free tier | Free–$30/month |
| CDN | Cloudflare free | Free |
| **Total** | | **~$100–200/month** |

> 💡 At startup stage, use **managed services** (MongoDB Atlas, Redis Cloud, Vercel) — don't manage servers yourself. Focus on product, not infra.

---

### 💼 Mid-Scale Phase (100K – 10M users)

| Component | Choice | Rough Cost |
|---|---|---|
| Frontend | Vercel Pro / AWS CloudFront + S3 | $100–500/month |
| Backend | Multiple EC2 instances + Load Balancer | $500–2000/month |
| Database | MongoDB Atlas M30 + Read Replicas | $500–2000/month |
| Cache | Redis Cluster (ElastiCache) | $200–500/month |
| CDN | AWS CloudFront | $100–300/month |
| **Total** | | **~$2,000–6,000/month** |

---

### 🏢 Large Scale Phase (100M – 500M users)

| Component | Choice | Rough Cost |
|---|---|---|
| Frontend | Global CDN + Edge rendering | $5,000+/month |
| Backend | 100s of servers + Kubernetes | $50,000+/month |
| Database | Sharded MongoDB + Replicas across regions | $20,000+/month |
| Cache | Multi-region Redis Cluster | $10,000+/month |
| Queues | Kafka for async processing | $5,000+/month |
| **Total** | | **$100,000+/month** |

> 💡 **Cloud Cost Thinking:** At scale, every millisecond of compute costs money. That's why caching, CDN, and efficient queries save huge amounts.

---

## 4. HIGH LEVEL DESIGN (HLD)

### 🧠 Think of it like this:
> HLD is like drawing a **city map** — you see the roads, districts, and connections.
> You don't see the inside of each building yet (that's LLD).

---

### 🖥️ Tech Stack Choices

| Layer | Technology | Why This Choice |
|---|---|---|
| Frontend | **Next.js** | SSR for SEO, fast initial load, SSG for static pages |
| Backend | **Node.js + Express** | Fast, lightweight, great for I/O heavy tasks like bookings |
| DB — Relational | **MySQL** | ACID transactions for Payments, Bookings, Users |
| DB — NoSQL | **MongoDB** | Flexible schema for Movies catalog, Reviews, Seat layouts |
| Cache | **Redis** | Ultra-fast, perfect for seat locking & session storage |
| Cloud | AWS / GCP | CDN, Load Balancer, Auto-scaling |

---

### 🗃️ Which Database for Which Service? (Polyglot Persistence)

> 💡 **What is Polyglot Persistence?**
> Using **different databases for different parts of the system**, each chosen for what it does best.
> Just like you use a knife to cut and a spoon to scoop — use the right tool for the right job.

> 🧠 **Analogy:** Think of MySQL as a **bank locker** (structured, safe, strict rules) and
> MongoDB as a **notebook** (flexible, fast to write, no fixed format).

| Service | Database | Why |
|---|---|---|
| **User Service** | ✅ MySQL | User accounts need strict schema, foreign keys, ACID |
| **Payment Service** | ✅ MySQL | Financial data — MUST have ACID transactions, no data loss |
| **Booking Service** | ✅ MySQL | Confirmed bookings need consistency + relational queries |
| **Show/Theatre Service** | ✅ MySQL | Shows relate to Theatres → Joins are natural here |
| **Movie Catalog Service** | ✅ MongoDB | Flexible schema: genres[], cast[], languages[], posters |
| **Reviews & Ratings** | ✅ MongoDB | User-generated content, variable structure |
| **Seat Layout Store** | ✅ MongoDB | Deeply nested seat maps — NoSQL handles this naturally |
| **Analytics / Events** | ✅ MongoDB | High-volume, schema-less event logs |
| **Session / Cache** | ✅ Redis | Ultra-fast in-memory, TTL-based, not for permanent storage |

```
Simple Rule of Thumb:

┌───────────────────────────────────────────────────────────┐
│  Use MySQL when:              Use MongoDB when:            │
│  ─────────────               ───────────────              │
│  • Money is involved          • Schema changes often       │
│  • Data is relational         • Nested/array fields needed │
│  • Strict consistency needed  • Catalog / content data     │
│  • Joins are frequent         • High-speed read ops        │
└───────────────────────────────────────────────────────────┘
```

---

### 🌐 Why Next.js? (SSR vs SSG vs CSR)

> **Analogy:** Think of a newspaper.
> - **SSG** = Newspaper printed last night (static, fast, same for everyone)
> - **SSR** = Newspaper printed fresh every morning (dynamic, SEO-friendly)
> - **CSR** = You write your own newspaper after buying (slow first load, interactive)

| Rendering | Full Form | When Used in This App | Why |
|---|---|---|---|
| **SSG** | Static Site Generation | Movie landing pages, genre pages | Pre-built at deploy time; SEO goldmine for Google |
| **SSR** | Server-Side Rendering | Movie detail page, show listings | Fresh data on every request; great for SEO |
| **CSR** | Client-Side Rendering | Seat selection, payment flow | Real-time interaction needed; no need for SEO here |

```
Example:
/movies/avengers         → SSG (same for everyone, pre-built)
/movies/avengers/shows   → SSR (different by date/city)
/booking/seat-selection  → CSR (real-time, user-specific)
```

> 🔑 **SEO Benefit:** Google cannot read JavaScript-rendered pages well. Using SSR/SSG ensures Google indexes movie pages properly, which drives organic traffic.

---

### 🏗️ Service-Level Architecture Diagram

```
                         ┌─────────────────────────────────────┐
                         │            USERS (Browser/App)       │
                         └──────────────────┬──────────────────┘
                                            │
                         ┌──────────────────▼──────────────────┐
                         │              CDN (CloudFront)        │
                         │    Serves static assets, images,     │
                         │    cached SSG pages globally         │
                         └──────────────────┬──────────────────┘
                                            │
                         ┌──────────────────▼──────────────────┐
                         │           Load Balancer              │
                         │   Distributes traffic across servers  │
                         └─────┬──────────────────┬────────────┘
                               │                  │
              ┌────────────────▼──┐        ┌──────▼─────────────┐
              │  Next.js Frontend  │        │  Next.js Frontend   │
              │  Server (SSR/API)  │        │  Server (SSR/API)   │
              └────────┬───────────┘        └────────┬────────────┘
                       │                             │
              ┌────────▼─────────────────────────────▼────────────┐
              │                  API Gateway                        │
              │     (Rate limiting, Auth, Routing to services)      │
              └──┬──────────┬───────────┬──────────┬──────────────┘
                 │          │           │          │
    ┌────────────▼──┐ ┌─────▼──────┐ ┌─▼────────┐ ┌▼───────────────┐
    │  User Service  │ │  Movie     │ │ Booking  │ │ Payment Service │
    │  (Auth/Profile)│ │  Service   │ │ Service  │ │ (UPI/Card etc) │
    └───────┬────────┘ └──────┬─────┘ └────┬─────┘ └───────┬────────┘
            │                 │             │               │
    ┌───────▼─────────────────▼─────────────▼───────────────▼────────┐
    │                     Redis Cache Layer                            │
    │          (Sessions, Seat Locks, Movie/Show Cache)                │
    └──────────────┬───────────────────────────────┬──────────────────┘
                   │                               │
    ┌──────────────▼───────────────┐  ┌────────────▼────────────────────┐
    │    MySQL (Relational DB)      │  │    MongoDB (Document DB)        │
    │  • Users & Auth               │  │  • Movie Catalog                │
    │  • Confirmed Bookings         │  │  • Theatre Seat Layouts         │
    │  • Payments (ACID!)           │  │  • Reviews & Ratings            │
    │  • Shows & Theatres           │  │  • Analytics Events             │
    └──────────────────────────────┘  └─────────────────────────────────┘
                                   │
    ┌──────────────────────────────▼──────────────────────────────────┐
    │               Notification Service (Async)                       │
    │         Email / SMS / Push via Kafka + Worker queues            │
    └─────────────────────────────────────────────────────────────────┘
```

---

### 🔄 Step-by-Step User Booking Flow

```
USER ACTION                     SYSTEM RESPONSE
───────────                     ───────────────
1. Open app                  →  CDN serves cached homepage (SSG)
2. Search "Avengers Mumbai"  →  API Gateway → Movie Service
                                Movie Service checks Redis cache first
                                Cache miss? → Fetch from MongoDB (catalog) → Store in Redis
3. Click on show (8 PM)      →  Show details from MySQL (shows table) — SSR page
4. Click "Select Seats"      →  CSR page loads seat map from MongoDB (seat layout doc)
5. Click seat A5             →  Booking Service → Lock seat A5 in Redis (10 min TTL)
                                Response: "Seat A5 held for you for 10 minutes"
6. User fills details        →  Frontend validation (client side)
7. Click "Pay ₹400"          →  Payment Service called
                                Payment Gateway (Razorpay/Stripe) processes
8. Payment SUCCESS           →  Booking Service:
                                - Confirm booking in MySQL (ACID transaction)
                                - Release Redis lock → Mark seat as BOOKED in MySQL
                                - Generate booking ID
9. Confirmation sent         →  Notification Service (async via queue):
                                - Send email with QR code
                                - Send SMS
10. User sees ticket         →  Booking confirmation page (CSR)
```

---

## 5. LOW LEVEL DESIGN (LLD)

### 🧠 Think of it like this:
> If HLD is the city map, LLD is the **blueprint of each building** — every room, every pipe, every wire.

---

### 🗄️ Database Design (Polyglot: MySQL + MongoDB)

> 🧠 **Key Insight:** We split data across two databases — MySQL for structured/transactional data, MongoDB for flexible catalog/content data.

---

#### ✅ MySQL Tables (Relational — for transactional, financial, structured data)

##### 👤 users table
```sql
CREATE TABLE users (
  id          BIGINT PRIMARY KEY AUTO_INCREMENT,
  name        VARCHAR(100)        NOT NULL,
  email       VARCHAR(255) UNIQUE NOT NULL,
  phone       VARCHAR(15),
  password_hash VARCHAR(255)      NOT NULL,
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_email (email)
);
```

##### 🏟️ theatres table
```sql
CREATE TABLE theatres (
  id       BIGINT PRIMARY KEY AUTO_INCREMENT,
  name     VARCHAR(200)  NOT NULL,
  city     VARCHAR(100)  NOT NULL,
  address  TEXT,
  lat      DECIMAL(9,6),
  lng      DECIMAL(9,6),
  INDEX idx_city (city)
);
```

##### 📺 screens table
```sql
CREATE TABLE screens (
  id           BIGINT PRIMARY KEY AUTO_INCREMENT,
  theatre_id   BIGINT NOT NULL,
  name         VARCHAR(50),
  total_seats  INT,
  FOREIGN KEY (theatre_id) REFERENCES theatres(id)
);
```

##### 🎟️ shows table
```sql
CREATE TABLE shows (
  id          BIGINT PRIMARY KEY AUTO_INCREMENT,
  movie_id    VARCHAR(24)   NOT NULL,   -- References MongoDB movie _id
  theatre_id  BIGINT        NOT NULL,
  screen_id   BIGINT        NOT NULL,
  show_time   DATETIME      NOT NULL,
  language    VARCHAR(20),
  format      ENUM('2D','3D','IMAX') DEFAULT '2D',
  price_premium DECIMAL(8,2),
  price_normal  DECIMAL(8,2),
  FOREIGN KEY (theatre_id) REFERENCES theatres(id),
  FOREIGN KEY (screen_id)  REFERENCES screens(id),
  INDEX idx_movie_city (movie_id, theatre_id),
  INDEX idx_show_time (show_time)
);
-- Note: movie_id is a VARCHAR storing MongoDB ObjectId as string
-- This is the BRIDGE between MySQL and MongoDB
```

##### 📋 bookings table
```sql
CREATE TABLE bookings (
  id           BIGINT PRIMARY KEY AUTO_INCREMENT,
  booking_ref  VARCHAR(30) UNIQUE NOT NULL,  -- e.g. BMS-2024-XYZ123
  user_id      BIGINT      NOT NULL,
  show_id      BIGINT      NOT NULL,
  seats        JSON        NOT NULL,          -- ["A1", "A2"]
  total_amount DECIMAL(10,2),
  status       ENUM('PENDING','CONFIRMED','CANCELLED') DEFAULT 'PENDING',
  qr_code      TEXT,
  created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (show_id) REFERENCES shows(id),
  INDEX idx_user (user_id),
  INDEX idx_status (status)
);
```

##### 💳 payments table
```sql
CREATE TABLE payments (
  id                    BIGINT PRIMARY KEY AUTO_INCREMENT,
  payment_ref           VARCHAR(50) UNIQUE NOT NULL,
  booking_id            BIGINT      NOT NULL,
  user_id               BIGINT      NOT NULL,
  amount                DECIMAL(10,2),
  method                ENUM('UPI','CARD','WALLET','NETBANKING'),
  gateway               VARCHAR(50),
  status                ENUM('PENDING','SUCCESS','FAILED','REFUNDED'),
  idempotency_key       VARCHAR(100) UNIQUE,  -- Prevents double charge!
  gateway_txn_id        VARCHAR(100),
  created_at            DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (booking_id) REFERENCES bookings(id),
  INDEX idx_booking (booking_id)
);
-- ACID properties here ensure money is NEVER double-charged or lost
```

> 💡 **Why JSON column for seats in bookings?** MySQL 5.7+ supports JSON columns.
> We store the seat array `["A1","A2"]` in MySQL to keep the booking fully in one ACID transaction.

---

#### ✅ MongoDB Collections (NoSQL — for flexible catalog & content data)

##### 🎬 movies collection
```json
{
  "_id": "ObjectId",
  "title": "Avengers: Endgame",
  "languages": ["Hindi", "English", "Tamil"],
  "genres": ["Action", "Sci-Fi"],
  "duration_mins": 182,
  "rating": "U/A",
  "posterUrl": "cdn.example.com/avengers.jpg",
  "trailerUrl": "youtube.com/watch?v=...",
  "releaseDate": "2024-05-01",
  "description": "After the devastating events of Avengers: Infinity War...",
  "cast": [
    { "name": "Robert Downey Jr.", "role": "Iron Man", "photoUrl": "..." },
    { "name": "Chris Evans",       "role": "Captain America", "photoUrl": "..." }
  ],
  "crew": [
    { "name": "Anthony Russo", "role": "Director" }
  ],
  "tags": ["sequel", "superhero", "blockbuster"],
  "avgRating": 4.7,
  "totalReviews": 128450
}
```
> 💡 **Why MongoDB for movies?** The `cast`, `genres`, `languages` are arrays that change per movie.
> Forcing this into MySQL tables would need multiple JOINs. MongoDB stores it naturally as one document.

##### 🪑 seat_layouts collection (per screen)
```json
{
  "_id": "ObjectId",
  "screen_id": 1,
  "theatre_id": 101,
  "layout": {
    "rows": ["A","B","C","D","E"],
    "seatsPerRow": 20,
    "categories": {
      "PREMIUM": { "rows": ["A","B"], "color": "#FFD700" },
      "NORMAL":  { "rows": ["C","D","E"], "color": "#4A90D9" }
    },
    "blockedSeats": ["A5", "B10"]
  }
}
```
> 💡 **Why MongoDB for seat layouts?** Complex nested structure — different theatres have different
> row configurations. A fixed MySQL schema would be rigid and wasteful here.

##### ⭐ reviews collection
```json
{
  "_id": "ObjectId",
  "movieId": "ObjectId",
  "userId": 456,
  "rating": 4.5,
  "title": "Absolutely Brilliant!",
  "body": "Best MCU movie ever made...",
  "likes": 234,
  "spoiler": false,
  "createdAt": "2024-05-02T09:00:00Z"
}
```

> 💡 **Seat Status in Redis (NOT in DB):** `AVAILABLE` → `LOCKED` (Redis TTL 10 min) → `BOOKED` (MySQL bookings table)

---

### 🌐 Key API Endpoints

```
AUTH APIS
──────────────────────────────────────────────────────────────
POST   /api/auth/register          Register new user
POST   /api/auth/login             Login, returns JWT token
POST   /api/auth/logout            Invalidate session

MOVIE APIS
──────────────────────────────────────────────────────────────
GET    /api/movies                 List all movies (with filters)
GET    /api/movies/:id             Get movie details
GET    /api/movies/:id/shows       Get shows for a movie
       Query: ?city=Mumbai&date=2024-05-01

THEATRE APIS
──────────────────────────────────────────────────────────────
GET    /api/theatres               List theatres by city
GET    /api/theatres/:id/shows     Shows at a specific theatre

BOOKING APIS
──────────────────────────────────────────────────────────────
GET    /api/shows/:showId/seats    Get seat availability for a show
POST   /api/bookings/lock-seats    Temporarily lock selected seats
       Body: { showId, seats: ["A1", "A2"] }
POST   /api/bookings/confirm       Confirm booking after payment
GET    /api/bookings/:bookingId    Get a specific booking
GET    /api/bookings/user/me       Get current user's bookings
DELETE /api/bookings/:bookingId    Cancel a booking

PAYMENT APIS
──────────────────────────────────────────────────────────────
POST   /api/payments/initiate      Start payment process
POST   /api/payments/verify        Verify payment from gateway webhook
GET    /api/payments/:paymentId    Get payment details
```

---

### 🔐 Seat Locking Algorithm (Concurrency Problem Solved!)

> 💡 **The Core Problem:** 1000 users click seat A5 at the same time. Who gets it?

#### ❌ Naive Approach (Wrong — Race Condition):
```
User 1 checks DB → seat is AVAILABLE
User 2 checks DB → seat is AVAILABLE  (same time!)
User 1 books it  → SUCCESS
User 2 books it  → SUCCESS  ← DOUBLE BOOKING! 😱
```

#### ✅ Redis-Based Seat Locking (Correct):

```
STEP 1: User clicks seat A5
STEP 2: Backend runs this Redis command atomically:
        SET seat:showId:A5 userId NX EX 600
        │                       │  │  │
        │                       │  │  └─ Expires in 600 seconds (10 min)
        │                       │  └──── NX = Only set if NOT exists
        │                       └─────── Value = userId
        └─────────────────────────────── Key = unique per show+seat

STEP 3: If Redis returns OK    → Seat locked for this user ✅
        If Redis returns NULL  → Seat already locked ❌ (show error)

STEP 4: User completes payment within 10 minutes
STEP 5: Payment SUCCESS → Update MongoDB: seat status = BOOKED
                        → Delete Redis lock key

STEP 6: Payment FAILS or Timeout → Redis TTL expires automatically
                                  → Seat becomes available again
```

#### Component-Level Diagram:

```
User Browser
    │
    │  POST /api/bookings/lock-seats
    ▼
Booking Service
    │
    ├──▶ Redis: SET seat:show123:A5 user456 NX EX 600
    │           ↳ Returns OK → lock acquired
    │           ↳ Returns NULL → seat taken!
    │
    ├─── If locked: Store "pending booking" in MongoDB
    │
    ▼
User sees: "Seat A5 reserved! Pay within 10 minutes"
    │
    │  POST /api/payments/initiate
    ▼
Payment Service
    │
    ├──▶ Payment Gateway (Razorpay)
    │
    ▼
Webhook: POST /api/payments/verify
    │
    ├──▶ If SUCCESS:
    │       MongoDB: Update seat A5 → BOOKED
    │       MongoDB: Create booking record
    │       Redis: DEL seat:show123:A5 (lock cleanup)
    │       Queue: Send email/SMS notification
    │
    └──▶ If FAILED:
            Redis: DEL seat:show123:A5 (release lock)
            MongoDB: Delete pending booking
            User sees: Payment failed, seat released
```

---

## 6. SCALABILITY DESIGN

### 🧠 Think of it like this:
> A single waiter can serve 10 tables. Add more waiters for more tables.
> Add a pre-prepared menu board (cache) so waiters don't go to the kitchen for common questions.

---

### 📐 Horizontal Scaling

```
Instead of making ONE server more powerful (vertical = limited)
Add MORE servers of the same size (horizontal = unlimited)

WITHOUT SCALING:            WITH HORIZONTAL SCALING:
┌──────────────┐            ┌──────────────┐
│  1 Big Server │            │  Server 1    │
│  Everything   │            │  Server 2    │  ← Load Balancer routes
│  runs here    │            │  Server 3    │     traffic evenly
└──────────────┘            │  Server N    │
                            └──────────────┘

Rule: Make services STATELESS (no session stored locally)
      → Store sessions in Redis (shared state)
      → Any server can handle any request
```

---

### ⚡ Caching Strategy with Redis

```
WHAT to cache:
┌─────────────────────────────────────────────────────────┐
│ Resource              │ TTL    │ Reason                  │
│───────────────────────│────────│─────────────────────────│
│ Movie list            │ 1 hour │ Changes rarely           │
│ Movie details         │ 1 hour │ Static info              │
│ Show timings by city  │ 5 min  │ Updates occasionally     │
│ Seat availability     │ 30 sec │ Changes frequently       │
│ User sessions         │ 24 hrs │ Avoid DB auth every time │
│ Seat locks            │ 10 min │ Concurrency control      │
└─────────────────────────────────────────────────────────┘

CACHE-ASIDE PATTERN (most common):
1. Request comes in
2. Check Redis first (cache hit? → return immediately)
3. Cache miss? → Fetch from MongoDB
4. Store in Redis with TTL
5. Return to user

          Request
             │
             ▼
        Redis Cache ──── HIT ────▶ Return Data ✅
             │
           MISS
             │
             ▼
          MongoDB
             │
             ▼
        Store in Redis
             │
             ▼
         Return Data ✅
```

---

### 🌍 CDN Usage with Next.js

```
WHAT CDN does:
"Instead of serving files from Mumbai server to a user in Chennai,
 put the files on a server IN Chennai (edge server)"

WITHOUT CDN:                    WITH CDN:
User (Chennai)                  User (Chennai)
  │                               │
  │ 1500km away                   │ 50km away
  ▼                               ▼
Server (Mumbai)               CDN Edge (Chennai)
  Response: 200ms               Response: 20ms 🚀

Next.js + CDN Strategy:
├── Static files (JS, CSS, images) → CloudFront/Cloudflare
├── SSG pages (movie landing pages) → CDN cached
├── SSR pages (show listings) → CDN with short TTL (5 min)
└── API responses → NOT cached at CDN (dynamic data)
```

---

### 🗃️ Database Scaling (MySQL + MongoDB)

#### MySQL Scaling
```
REPLICATION (Read Scaling):
┌──────────────────────────────────────────────────┐
│                                                    │
│   MySQL Primary ──replicates──▶ Read Replica 1   │
│                  ──replicates──▶ Read Replica 2   │
│                                                    │
│   Writes → Primary only                           │
│   Reads  → Replicas (80% of all traffic)          │
│   Orchestrated by: ProxySQL or AWS RDS            │
└──────────────────────────────────────────────────┘

PARTITIONING (MySQL doesn't shard natively):
- Partition bookings table by created_at (month)
- Old months → archived to cold storage
- Active month → hot partition, fast queries

  bookings_2024_Jan  bookings_2024_Feb  bookings_2024_Mar
       (archived)         (archived)        (active)
```

#### MongoDB Scaling
```
SHARDING (Natural fit for MongoDB at 500M users):
Split data across multiple MongoDB instances by shard key

Movies collection → Shard key: genre or language
Reviews collection → Shard key: movieId

┌─────────────────────────────────────────────┐
│  Query Router (mongos)                       │
│         │                                    │
│    ┌────┼────┐                               │
│    ▼    ▼    ▼                               │
│  Action Drama Comedy    (Shards by genre)    │
│  Shard  Shard  Shard                         │
└─────────────────────────────────────────────┘

REPLICATION (HA for MongoDB):
Each shard is itself a 3-node replica set:
   Shard 1: Primary → Replica → Replica
   Shard 2: Primary → Replica → Replica
```

#### Summary: When Does Each Scale?
```
┌─────────────────────────────────────────────────────────┐
│ Users       │ MySQL                │ MongoDB             │
│─────────────│──────────────────────│─────────────────────│
│ 0 – 100K    │ Single instance      │ Single instance     │
│ 100K – 10M  │ + Read replicas      │ + Read replicas     │
│ 10M – 100M  │ + Partitioning       │ + Sharding begins   │
│ 100M – 500M │ Managed RDS cluster  │ Global clusters     │
└─────────────────────────────────────────────────────────┘
```

---

## 7. RELIABILITY & FAULT TOLERANCE

### 🧠 Think of it like this:
> A good restaurant has a backup chef, and if the power goes out, they have a generator. Plan for failure.

---

### 💳 What Happens If Payment Fails?

```
SCENARIO: User pays, payment gateway crashes mid-transaction

            Payment Initiated
                   │
                   ▼
        Payment Gateway crashes ❌
                   │
    ┌──────────────▼──────────────┐
    │   Booking stays in          │
    │   "PENDING" state           │
    │   in MongoDB                │
    └──────────────┬──────────────┘
                   │
        ┌──────────▼──────────┐
        │   RETRY MECHANISM    │
        │  (Exponential Backoff)│
        │  Try after:          │
        │   1s → 2s → 4s → 8s │
        └──────────┬──────────┘
                   │
         ┌─────────┴─────────┐
         │                   │
      Succeeds           Still fails
         │                   │
     Confirm              Release seat
     booking              Refund if charged
```

---

### 🖥️ What Happens If Server Crashes?

```
SCENARIO: Booking Service server goes down

WITHOUT Fault Tolerance:    WITH Fault Tolerance:
User gets error ❌           Load Balancer detects crash
                              Redirects to healthy server ✅
                              Health checks every 30 seconds
                              Auto-healing (Kubernetes restarts pod)

TECHNIQUES:
1. Multiple instances of each service
2. Load balancer with health checks
3. Database replicas (auto-failover)
4. Redis Sentinel / Redis Cluster (Redis HA)
5. Circuit Breaker Pattern:
   - If Payment Service fails 5 times in a row
   - Stop sending requests for 30 seconds
   - Prevent cascade failures
```

---

### 🔄 Retry & Fallback Strategies

```
RETRY:
- Payment: Retry 3 times with exponential backoff
- Notification: Retry 5 times (email is not critical)
- Booking confirmation: Idempotent (safe to retry, same result)

FALLBACK:
- Movie images fail to load → Show placeholder image
- Recommendations fail → Show popular movies instead
- Payment gateway down → Show "Try again later" (don't crash)

IDEMPOTENCY (critical for payments!):
- Every payment request has a unique idempotency key
- If same request sent twice → process only once
- Prevents double charging the user ✅
```

---

## 8. FLEXIBILITY & EXTENSIBILITY

### 🧠 Think of it like this:
> Build a house with extra electrical outlets. Later you can add ACs, heaters without rewiring.

---

### 🎁 Adding Offers & Discount System

```
New Microservice: Offer Service
├── GET /api/offers?userId=&movieId=  → Get applicable offers
├── POST /api/offers/apply            → Apply offer to booking
└── Admin: Create/edit/delete offers

Integration:
Booking Service → calls Offer Service before payment
MongoDB: offers collection
Redis: Cache active offers (avoid DB hit every booking)

Design: Rule-based engine
{
  "offerId": "BLOCKBUSTER50",
  "condition": {
    "movieId": "avengers",
    "minAmount": 500,
    "paymentMethod": "UPI"
  },
  "discount": { "type": "PERCENT", "value": 50, "maxDiscount": 200 }
}
```

---

### 🔔 Adding Notifications System

```
Use Event-Driven Architecture:
Booking Confirmed → Emit Event → Notification Workers pick up

                 Booking Service
                       │
                 Emit Event to
                  Message Queue
                 (Kafka/RabbitMQ)
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
    Email Worker  SMS Worker  Push Notification
    (SendGrid)    (Twilio)    Worker (FCM)

Why Queue?
- Notification doesn't slow down booking flow
- If email service is down, messages wait in queue
- Retry failed notifications automatically
```

---

### 🌐 Adding Multi-Language Support

```
Next.js i18n Configuration (next.config.js):

module.exports = {
  i18n: {
    locales: ['en', 'hi', 'ta', 'te', 'mr'],
    defaultLocale: 'en',
    localeDetection: true
  }
}

File Structure:
/public/locales/
  ├── en/common.json   { "book_now": "Book Now" }
  ├── hi/common.json   { "book_now": "अभी बुक करें" }
  ├── ta/common.json   { "book_now": "இப்போது புக் செய்" }

URL Structure:
example.com/en/movies/avengers
example.com/hi/movies/avengers    ← Hindi version
example.com/ta/movies/avengers    ← Tamil version

SEO Benefit: hreflang tags tell Google which language version to show
```

---

### 🔍 SEO Improvements with Next.js

```javascript
// pages/movies/[id].js — SSR for movie pages
export async function getServerSideProps({ params }) {
  const movie = await fetchMovie(params.id);
  return { props: { movie } };
}

export default function MoviePage({ movie }) {
  return (
    <>
      <Head>
        <title>{movie.title} - Book Tickets | MovieApp</title>
        <meta name="description" content={`Book tickets for ${movie.title}. ${movie.description.slice(0, 155)}`} />
        <meta property="og:title" content={movie.title} />
        <meta property="og:image" content={movie.posterUrl} />
        <meta property="og:type" content="video.movie" />
        {/* Structured Data for Google Rich Results */}
        <script type="application/ld+json">{JSON.stringify({
          "@context": "https://schema.org",
          "@type": "Movie",
          "name": movie.title,
          "image": movie.posterUrl,
          "dateCreated": movie.releaseDate
        })}</script>
      </Head>
      {/* Page content */}
    </>
  );
}
```

---

## 9. DEV-FRIENDLY PRACTICES

### 📁 Project Structure

```
movie-booking-app/
│
├── 📁 frontend/                    (Next.js App)
│   ├── pages/
│   │   ├── index.js               Home page (SSG)
│   │   ├── movies/[id].js         Movie detail (SSR)
│   │   ├── booking/[showId].js    Seat selection (CSR)
│   │   └── my-bookings.js         User bookings (CSR)
│   ├── components/
│   │   ├── SeatMap.jsx
│   │   ├── MovieCard.jsx
│   │   └── BookingTimer.jsx
│   ├── hooks/
│   │   └── useSeatLock.js
│   ├── utils/
│   │   └── api.js                 Axios wrapper
│   └── public/locales/            i18n translations
│
├── 📁 backend/                     (Node.js + Express)
│   ├── services/
│   │   ├── user-service/
│   │   │   ├── index.js
│   │   │   ├── routes/auth.js
│   │   │   └── models/User.js
│   │   ├── movie-service/
│   │   ├── booking-service/
│   │   └── payment-service/
│   ├── shared/
│   │   ├── redis.js               Redis client setup
│   │   ├── db.js                  MongoDB connection
│   │   ├── logger.js              Winston logger
│   │   └── middleware/
│   │       ├── auth.js            JWT middleware
│   │       └── rateLimiter.js
│   └── gateway/                   API Gateway
│
├── 📁 infrastructure/
│   ├── docker-compose.yml
│   ├── kubernetes/
│   └── terraform/                 IaC (optional)
│
└── 📁 docs/
    └── System Design/
        └── 03_Movie_Ticket_System.md
```

---

### 🚀 CI/CD Pipeline

```
Developer pushes code to GitHub
            │
            ▼
     GitHub Actions Triggered
            │
    ┌───────┼────────────────┐
    ▼       ▼                ▼
  Lint    Unit Tests      Type Check
  (ESLint) (Jest)         (TypeScript)
    │
    └──── All Pass? ──── No → Block merge ❌
              │
             Yes
              │
              ▼
       Build Docker Image
              │
              ▼
       Push to Registry (ECR/DockerHub)
              │
              ▼
       Deploy to Staging (auto)
              │
              ▼
       Run Integration Tests
              │
              ▼
       Manual Approval Gate 👆
              │
              ▼
       Deploy to Production ✅
       (Blue-Green deployment → zero downtime)
```

---

### 📊 Logging & Monitoring

```
LOGGING (What happened):
- Use Winston (Node.js) for structured JSON logs
- Log: Request ID, User ID, Action, Duration, Status
- Send logs to → ELK Stack (Elasticsearch + Logstash + Kibana)

Example log:
{
  "timestamp": "2024-05-01T20:01:05Z",
  "level": "info",
  "service": "booking-service",
  "requestId": "req-abc123",
  "userId": "user-456",
  "action": "SEAT_LOCK",
  "showId": "show-789",
  "seats": ["A1", "A2"],
  "duration_ms": 45,
  "status": "SUCCESS"
}

MONITORING (Is system healthy):
- Use Prometheus + Grafana
- Metrics to track:
  ├── Response time (P50, P90, P99)
  ├── Error rate (should be < 0.1%)
  ├── Active seat locks in Redis
  ├── Payment success rate
  └── DB query times

ALERTING:
- Error rate > 1%           → Alert engineering team
- Response time > 500ms     → Alert on-call dev
- Redis memory > 80%        → Scale Redis
- Payment failure spike     → Alert immediately
```

---

## 10. FINAL NOTES (BEGINNER FRIENDLY)

### 📝 Summary
> You just learned how to design a system like BookMyShow from scratch!
> The key insight: **start simple, scale gradually**.

| Section | Key Lesson |
|---|---|
| Requirements | Know WHAT to build before HOW |
| Scale | Estimate traffic early to plan infra |
| HLD | Design services to be independent |
| LLD | Think about concurrency from day 1 |
| Scalability | Cache aggressively, scale horizontally |
| Reliability | Plan for failure, not against it |
| Extensibility | Design for change, not just today |

---

### 🏆 Key Takeaways

1. **Seat Locking with Redis** is the heart of this system. Get this right.
2. **Idempotency in payments** prevents double charges. Always use idempotency keys.
3. **Cache heavily** — 80% of traffic is read (browsing movies), cache it all.
4. **Next.js SSR/SSG** is a powerful SEO tool. Use SSG for static pages, SSR for dynamic ones.
5. **Async everything non-critical** — notifications, analytics shouldn't slow down booking.
6. **Design for failure** — every component WILL fail someday. Handle it gracefully.

---

### 🚫 Common Beginner Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---|---|---|
| No seat locking | Race conditions → double booking | Redis atomic lock with TTL |
| Sync notifications | Slows down booking by 2-3 seconds | Async via message queue |
| No caching | DB hit on every request → DB gets crushed | Cache-aside with Redis |
| SSR for everything | Slow, no CDN caching benefit | Mix SSR, SSG, CSR wisely |
| No idempotency | Payment charged twice on retry | Unique idempotency keys |
| Single point of failure | One server down = app down | Multiple instances + LB |
| Storing passwords in plain text | Security disaster | bcrypt hash always |
| No rate limiting | DDoS makes system crash | Rate limit at API Gateway |
| Ignoring indexes in MongoDB | Queries become very slow | Index on frequently queried fields |
| No monitoring | Flying blind in production | Prometheus + Grafana alerts |

---

## 11. SCENARIO-BASED Q&A

> 🎯 These are real interview questions. Practice answering them out loud!

---

### Q1: What happens if 1,000 users try to book the same seat simultaneously?

**Answer:**
Without protection, this causes a race condition and double bookings. We solve this using **Redis atomic locking**:
- Each seat lock is stored in Redis with the key `seat:{showId}:{seatId}`
- We use `SET key value NX EX 600` command — this is **atomic** in Redis
- `NX` means "set only if Not eXists" — so only ONE user's request will succeed
- The remaining 999 users get a "Seat unavailable" response immediately
- If the winner doesn't pay within 10 minutes, the TTL expires and the seat is released

**Analogy:** It's like a tokenized queue — only one person gets the token; everyone else is told to wait.

---

### Q2: How would you handle SEO for movie pages?

**Answer:**
Using **Next.js SSR and SSG**:
- **Movie landing pages** → SSG: Pre-built at deploy time. Google can crawl them easily.
- **Show listings** → SSR: Fresh data (showtimes change daily), rendered on server
- Add proper `<title>`, `<meta description>`, Open Graph tags in `<Head>`
- Add **JSON-LD structured data** so Google shows rich results (star ratings, showtimes)
- Use **hreflang** tags for multi-language pages
- Canonical URLs to avoid duplicate content penalties
- Fast load time (Core Web Vitals score) via CDN + image optimization (`next/image`)

---

### Q3: How would you handle traffic spikes during big movie releases?

**Answer:**
Multiple strategies working together:
1. **Auto-scaling** — Cloud (AWS) automatically adds more servers when CPU > 70%
2. **Aggressive caching** — Movie details, show listings cached in Redis and CDN
3. **Queue-based seat locking** — Redis handles thousands of concurrent seat requests
4. **Rate limiting** — Limit each user to X requests/second at API Gateway level
5. **CDN for static content** — Movie posters, homepage load from edge servers near the user
6. **Database read replicas** — Spike in reads goes to replicas, not primary DB
7. **Pre-warming** — Before a known big release (like KGF 3), scale up proactively

**Analogy:** Like a cricket stadium — you know when the big match is. You hire extra security, open more gates, and pre-stock the snack bars BEFORE the crowd arrives.

---

### Q4: How would you prevent a user from being double-charged?

**Answer:**
Using **Idempotency Keys**:
- When the payment request is made, generate a unique key: `idem_{userId}_{bookingId}_{timestamp}`
- Send this key with every payment request to the gateway
- If the same request is retried (network failure, user clicks Pay twice), the gateway recognizes the key and returns the previous result
- On our side, before processing payment, check if a payment with this bookingId already exists in a `COMPLETED` state
- This is also why we store `bookingId` as a unique index in the payments collection

---

### Q5: What would you change if you had to add a "food ordering" feature?

**Answer:**
Classic extensibility question:
1. Create a new **Food Service** microservice (independent, deployable separately)
2. Add a `FoodOrder` collection in MongoDB
3. New APIs: `GET /api/shows/{showId}/food-menu`, `POST /api/food-orders`
4. Food ordering is **optional** — add it as a separate step in the booking flow (after seat selection, before payment)
5. Bundle food total with ticket amount before sending to payment service
6. No changes needed to existing Booking, Movie, or User services

**Key principle:** Open-Closed Principle — open for extension, closed for modification.

---

### Q6: How would you design for offline support (no internet)?

**Answer:**
- Use **Service Workers** (PWA) to cache the last-seen movie listings
- Store booking confirmation in **localStorage** for offline viewing
- QR code is downloaded and cached once booking is confirmed
- Show "You're offline" indicator with cached data still visible
- This is more of a frontend concern; the backend doesn't need changes

---

### Q7: How would you ensure data consistency across services?

**Answer:**
Using the **Saga Pattern**:
1. Booking Service creates PENDING booking
2. Payment Service processes payment
3. If payment succeeds → Booking Service confirms → Notification Service sends ticket
4. If any step fails → Saga triggers compensating transactions:
   - Payment failed → Release seat lock, refund if any charge happened
   - Notification failed → Retry asynchronously (non-critical)

This avoids distributed transactions (2PC) which are slow and complex.

---

*End of Document*

---

> 📌 **Study Tip:** Read this document once for understanding, then come back and try to redraw all the diagrams from memory. That's the best way to remember system design concepts.

> 🎯 **Interview Tip:** In interviews, always start with requirements, estimate scale, then go HLD → LLD. Show you think in systems, not just code.
