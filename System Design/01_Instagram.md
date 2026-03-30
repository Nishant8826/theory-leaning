# Instagram System Design

## Introduction
Welcome to one of the most interesting case studies in System Design! If you've ever used Instagram, you know it’s not just a place to see pretty photos. Behind that smooth "Double Tap to Like," there is a massive engine handling millions of uploads every minute.

### What is Instagram?
At its core, Instagram is a **Photo and Video Sharing Social Network**. It focuses on visual storytelling and mobile-first experiences.

### Key Features
1.  **User Authentication:** Signing up, logging in, and keeping your profile safe.
2.  **Posting Images/Videos:** Uploading your media to share with the world.
3.  **Feed:** A personalized list of photos/videos from people you follow.
4.  **Likes & Comments:** Interacting with posts (The "Social" part).
5.  **Follow System:** Connecting with friends and creators.

---

## Functional Requirements
*(What the system **must** do for the user)*
*   Users should be able to upload photos/videos.
*   Users can follow/unfollow other users.
*   Users should have a "Home Feed" showing posts from everyone they follow.
*   Users can like and comment on posts.
*   Users can search for other people or hashtags.

## Non-Functional Requirements
*(How the system should **behave** behind the scenes)*
*   **Scalability:** The system must handle 500 million+ active users.
*   **High Availability:** The app should never be "down." If one server crashes, the user shouldn't even notice.
*   **Performance (Low Latency):** The feed should load in less than 200ms. Nobody likes a spinning wheel!
*   **Reliability:** If you upload a photo, it must **never** be lost.
*   **Consistency:** It's okay if a "Like" takes a few seconds to show up for your friend (Eventual Consistency), but the photo must be there!

---

## High-Level Design (HLD)

### System Overview
Imagine a giant post office. One person (The Client/Your Phone) sends a letter (The Post). The post office (The Backend) checks who it's for, saves a copy in a file cabinet (The Database), puts the heavy photo in a warehouse (Storage), and then makes sure everyone who is "subscribed" to that person gets a copy in their mailbox (The Feed).

### Core Components

1.  **Frontend (Next.js)**
    *   **What:** The "face" of the app you see on your screen.
    *   **Why:** To give users a beautiful and fast interface.
    *   **How:** It handles the layout, buttons, and displays data it gets from the backend.

2.  **Backend (Node.js)**
    *   **What:** The "brain" of the system.
    *   **Why:** To process logic (e.g., "Is this password correct?" or "Save this comment").
    *   **How:** It receives requests, talks to the database, and sends answers back to the frontend.

3.  **Database (SQL + MongoDB)**
    *   **What:** The "memory" where all data is kept.
    *   **Why:** To store user info, follows, and post details.
    *   **How:** We use **SQL** for strict logic (Follows/Relationships) and **NoSQL (MongoDB)** for flexible data (Posts/Comments).

4.  **Storage (AWS S3)**
    *   **What:** A giant "hard drive" in the cloud.
    *   **Why:** Databases are good for text, but bad for heavy photos/videos.
    *   **How:** We save the actual image in S3 and just save its "link" in the database.

5.  **CDN (Content Delivery Network)**
    *   **What:** A network of servers all over the world.
    *   **Why:** If you are in India, you shouldn't have to wait for an image to travel from a server in the USA.
    *   **How:** It keeps a "copy" of the image in a server near you, making it load instantly.

6.  **Load Balancer**
    *   **What:** A traffic controller.
    *   **Why:** To prevent one server from getting overwhelmed.
    *   **How:** It splits incoming users across 100 different servers so they all share the load.

7.  **API Gateway**
    *   **What:** The receptionist at the front door.
    *   **Why:** To check security, rate-limiting, and route you to the right service.
    *   **How:** It makes sure you are allowed to enter before letting you talk to the backend.

8.  **Cache (Redis)**
    *   **What:** A super-fast "short-term memory" that sits between the backend and the database.
    *   **Why:** Reading from a database is slow (like looking in a file cabinet). Redis keeps the most popular data in RAM so it loads 100x faster.
    *   **How:** When someone asks for a post, we first check Redis. If it's there ("Cache Hit"), we return it instantly. If not ("Cache Miss"), we read from the database, save a copy in Redis, and then return it.

---

## Architecture Diagram (Text Based)

```text
[ User's Phone / Browser (Next.js) ]
               ↓
       [ Load Balancer ]  ← (Spreads the traffic across servers)
               ↓
         [ API Gateway ]  ← (Security, Auth, Rate Limiting, Routing)
               ↓
    [ Backend (Express.js / Node.js) ]
         ↓        ↓            ↓
  [ Cache ]  [ Database ]  [ Storage ]
  (Redis)    (SQL + MongoDB)  (AWS S3)
                                ↓
                            [ CDN ]  ← (Fast delivery to users worldwide)
```

**Detailed Flow:**
```text
User Action → Load Balancer → API Gateway → Auth Check (JWT)
  → Route to correct Backend Service
  → Check Cache (Redis) first
  → If not in cache → Query Database (SQL/MongoDB)
  → If media needed → Fetch from CDN/S3
  → Return Response to User
```

---

## Feature-wise Design (VERY IMPORTANT)

This section explains HOW each feature works from the user's tap to the server's response.

---

### 1. User Authentication (Signup / Login / Security)

**What:** The system that verifies "Are you who you say you are?"

**How Signup Works (Step-by-Step):**
1. User fills in username, email, and password on the frontend (Next.js).
2. Frontend sends a `POST /signup` request to the backend.
3. Backend checks: Does this email already exist in SQL? If yes → return error.
4. Backend **hashes** the password using **bcrypt** (never store plain text passwords!).
5. Backend creates a new row in the `users` SQL table.
6. Backend generates a **JWT token** and sends it back to the user.
7. Frontend stores this token in an **HttpOnly cookie** (safe from hackers).

**How Login Works:**
1. User enters email + password → `POST /login`.
2. Backend finds the user by email in SQL.
3. Backend uses `bcrypt.compare()` to check if the password matches the hash.
4. If it matches → generate a new JWT token and return it.
5. If not → return "Invalid credentials."

**What is JWT (JSON Web Token)?**
Think of it like a **movie ticket**. When you buy the ticket (login), the theater gives you a stamped ticket. Every time you want to enter a screen (make an API call), you show the ticket. The stamp proves it's real.

```javascript
// JWT contains 3 parts:
// HEADER.PAYLOAD.SIGNATURE
// Example payload:
{
  "userId": 101,
  "username": "nishant_dev",
  "iat": 1700000000,    // Issued At (when token was created)
  "exp": 1700086400     // Expires At (token dies after 24 hours)
}
```

**Password Security:**
```javascript
// NEVER do this:
const password = "mypass123"; // ❌ Plain text

// ALWAYS do this:
const bcrypt = require('bcrypt');
const hashedPassword = await bcrypt.hash("mypass123", 10); // ✅ Hashed
// Result: "$2b$10$N9qo8uLOickgx2ZMRZoMye..." (unreadable gibberish)
```

**Security Layers:**
- **Rate Limiting:** Max 5 login attempts per minute (prevents brute force).
- **HttpOnly Cookies:** JavaScript on the page can't steal the token.
- **Token Expiry:** Tokens die after 24 hours, so stolen tokens become useless.
- **Refresh Tokens:** A longer-lived token used to get a new JWT without re-logging in.

---

### 2. Post Upload (Image / Video)

**What:** The entire journey of a photo from your phone to someone else's screen.

**Upload Flow (Step-by-Step):**
```text
User taps "Share"
  → Phone sends photo + caption to Backend
  → Backend validates (is it an image? is it under 10MB?)
  → Backend resizes the image (using Sharp library)
  → Backend uploads resized images to AWS S3
  → S3 returns the URL (e.g., "https://s3.aws.com/thumb_abc.jpg")
  → Backend saves post metadata to MongoDB (URL, caption, userId, timestamp)
  → Backend triggers "Fan-out" → pushes post ID to followers' feeds in Redis
  → Returns success to the user's phone
```

**Why upload to S3 and not the database?**
- Databases are for **text** (fast to search, small in size).
- Images are **binary blobs** (5-10 MB each). Storing millions of these in a database would make it extremely slow and expensive.
- S3 is designed for files — it's cheap, reliable, and can store unlimited data.

**Multiple Image Sizes (Why?):**
| Version | Size | Used When |
|:---|:---|:---|
| `thumb_` | 150x150 | Profile grid, search results |
| `standard_` | 1080x1080 | Feed view |
| `original_` | Full size | When user taps to zoom |

This saves bandwidth. Why load a 5MB original when you're just scrolling?

---

### 3. Feed System (Personalized Timeline)

**What:** The list of posts you see when you open Instagram. It's personalized — you only see posts from people you follow.

**The Challenge:** If you follow 500 people, and each of them posts 3 times a day, that's 1,500 potential posts. The system needs to decide **which** posts to show you and in **what order** — all in under 200ms.

**Three Approaches:**

| Approach | How it Works | Good For | Bad For |
|:---|:---|:---|:---|
| **Pull** | When you open the app, backend searches DB for all followed users' posts | Celebrities (many followers) | Slow for users |
| **Push** | When someone posts, backend pre-delivers it to all followers' feeds | Normal users (few followers) | Celebrities (millions of followers) |
| **Hybrid** | Push for normal users + Pull for celebrities on read | Everyone | More complex to build |

*(Detailed code for each approach is in the Code section below)*

---

### 4. Likes & Comments

**What:** The interaction system — how users react to posts.

**How "Like" Works:**
1. User double-taps a post → `POST /like` → Backend.
2. Backend checks: Has this user already liked this post? (Prevent duplicate likes).
3. If not → Insert a record in the `likes` MongoDB collection.
4. Increment the `likes_count` in the post document.
5. **(Optimization):** Update the count in **Redis** first (instant), then sync to MongoDB in background.

**MongoDB Likes Collection:**
```json
{
  "like_id": "lk_001",
  "post_id": "p999",
  "user_id": 101,
  "created_at": "2024-06-15T10:30:00Z"
}
```

**How "Comment" Works:**
1. User types a comment → `POST /comment` → Backend.
2. Backend validates (is the comment too long? does it contain banned words?).
3. Save the comment in the `comments` MongoDB collection.
4. Increment `comments_count` on the post.

**MongoDB Comments Collection:**
```json
{
  "comment_id": "cm_001",
  "post_id": "p999",
  "user_id": 205,
  "text": "Amazing shot! 🔥",
  "created_at": "2024-06-15T11:00:00Z",
  "replies": [
    {
      "user_id": 101,
      "text": "Thanks bro!",
      "created_at": "2024-06-15T11:05:00Z"
    }
  ]
}
```

**Why MongoDB for Likes & Comments?**
- A single post can have **millions** of likes and **thousands** of comments.
- MongoDB handles this "one-to-many" relationship much better than SQL.
- We can nest replies inside comments (embedded documents) for fast reads.

---

### 5. Follow System

**What:** The connection between users — who follows whom.

**How it Works:**
1. User A taps "Follow" on User B's profile → `POST /follow`.
2. Backend checks: Is User A already following User B? If yes → return error.
3. Backend inserts a new row in the SQL `followers` table.
4. Increment `followers_count` for User B and `following_count` for User A.

**Why SQL for Follow System?**
- Following is a **relationship** — "User A follows User B." This is exactly what SQL (Relational Database) is built for.
- We need **strict consistency** here. If you unfollow someone, it must happen immediately. No "eventual consistency" allowed.
- SQL supports **JOINs** which make queries like "Find all mutual followers" very efficient.

**SQL Query Examples:**
```sql
-- Get all people that User 101 follows
SELECT u.username, u.profile_pic
FROM followers f
JOIN users u ON f.following_id = u.user_id
WHERE f.follower_id = 101;

-- Get all followers of User 205
SELECT u.username
FROM followers f
JOIN users u ON f.follower_id = u.user_id
WHERE f.following_id = 205;

-- Check if User 101 follows User 205
SELECT EXISTS(
  SELECT 1 FROM followers
  WHERE follower_id = 101 AND following_id = 205
);

-- Get mutual followers (people both User 101 and User 205 follow)
SELECT f1.following_id
FROM followers f1
JOIN followers f2 ON f1.following_id = f2.following_id
WHERE f1.follower_id = 101 AND f2.follower_id = 205;
```

---

## Database Design

### Why use BOTH SQL & MongoDB?

| Feature | SQL (PostgreSQL) | MongoDB |
|:---|:---|:---|
| **Best for** | Strict relationships (users, follows) | Flexible, heavy data (posts, comments) |
| **Schema** | Fixed columns — every row looks the same | Flexible — each document can be different |
| **Scaling** | Harder (vertical first, then sharding) | Easier (horizontal sharding built-in) |
| **Queries** | JOINs across tables | Fast reads on single collections |
| **Example** | "User A follows User B" | "Post with 5 images and 1000 comments" |

**Simple Rule:** If the data is about **relationships** → SQL. If it's about **content** → MongoDB.

---

### SQL Tables

**Users Table:**
```sql
CREATE TABLE users (
    user_id       SERIAL PRIMARY KEY,
    username      VARCHAR(30) UNIQUE NOT NULL,
    email         VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name  VARCHAR(50),
    bio           TEXT,
    profile_pic   VARCHAR(500),           -- S3 URL
    followers_count   INT DEFAULT 0,
    following_count   INT DEFAULT 0,
    is_verified   BOOLEAN DEFAULT FALSE,
    is_private    BOOLEAN DEFAULT FALSE,
    created_at    TIMESTAMP DEFAULT NOW(),
    updated_at    TIMESTAMP DEFAULT NOW()
);

-- Index for fast login lookup
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

| user_id | username | email | password_hash | followers_count |
| :--- | :--- | :--- | :--- | :--- |
| 101 | nishant_dev | n@test.com | $2b$10... | 5200 |

**Followers Table:**
```sql
CREATE TABLE followers (
    id            SERIAL PRIMARY KEY,
    follower_id   INT NOT NULL REFERENCES users(user_id),  -- The person who follows
    following_id  INT NOT NULL REFERENCES users(user_id),  -- The person being followed
    created_at    TIMESTAMP DEFAULT NOW(),
    UNIQUE(follower_id, following_id)  -- Prevent duplicate follows
);

-- Index for fast "who do I follow?" and "who follows me?" queries
CREATE INDEX idx_followers_follower ON followers(follower_id);
CREATE INDEX idx_followers_following ON followers(following_id);
```

| id | follower_id | following_id | created_at |
| :--- | :--- | :--- | :--- |
| 1 | 101 | 205 | 2024-01-01 |
| 2 | 205 | 101 | 2024-01-02 |

**What are Indexes?**
Think of an index like the "Table of Contents" in a book. Without it, the database reads ALL rows to find your data (slow). With it, it jumps directly to the right row (fast). We index `email` because every login searches by email.

---

### MongoDB Collections

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

**Comments Collection (Separate from Posts for scalability):**
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

**Why separate Comments from Posts?**
If we embed comments inside the post document, a post with 50,000 comments would become a single massive document (MongoDB has a 16MB limit per document). By storing comments in a separate collection, we can paginate them (load 20 at a time).

---

## Low-Level Design (LLD)

### API Design (The Conversation)
APIs are like conversations between your phone and the server. In our **Express.js** backend, we define "Routes" for these conversations.

#### 1. POST `/signup` (Create Account)
*   **Request Body:** `{ "username": "nishant", "email": "n@test.com", "password": "mypass123" }`
*   **Logic:**
    1.  Validate input (is email valid? is password 8+ characters?).
    2.  Check if email/username already exists in SQL.
    3.  Hash password with bcrypt.
    4.  Insert new user into SQL `users` table.
    5.  Generate JWT token.
*   **Response:** `201 Created` → `{ "token": "eyJhb...", "user": { "id": 101, "username": "nishant" } }`
*   **Error:** `409 Conflict` → `{ "error": "Email already exists" }`

#### 2. POST `/login` (Authenticate)
*   **Request Body:** `{ "email": "n@test.com", "password": "mypass123" }`
*   **Logic:**
    1.  Find user by email in SQL.
    2.  Compare password hash with bcrypt.
    3.  Generate JWT token.
*   **Response:** `200 OK` → `{ "token": "eyJhb...", "user": { ... } }`
*   **Error:** `401 Unauthorized` → `{ "error": "Invalid credentials" }`

#### 3. POST `/create-post` (Upload your content)
*   **Request Body:** `FormData` containing the Image file and `caption`.
*   **Headers:** `Authorization: Bearer <JWT_TOKEN>`
*   **Logic:**
    1.  **Auth Check:** Decode JWT → is the user logged in?
    2.  **File Validation:** Is it an image/video? Is it under 10MB?
    3.  **Process:** Shrink the photo using Sharp library.
    4.  **Upload:** Put resized files in S3 → get URLs back.
    5.  **Save:** Put URLs + caption into MongoDB `posts` collection.
    6.  **Fan-out:** Push post ID to followers' feeds in Redis.
*   **Response:** `201 Created` → `{ "postId": "p999", "imageUrl": "..." }`

#### 4. GET `/feed?page=1&limit=20` (Get your timeline)
*   **Headers:** `Authorization: Bearer <JWT_TOKEN>`
*   **Logic:**
    1.  Get pre-built feed from Redis (Push model results).
    2.  Pull latest celebrity posts from MongoDB (Pull model).
    3.  Merge, sort by time, paginate.
*   **Response:** `200 OK` → `{ "posts": [...], "nextPage": 2, "hasMore": true }`

#### 5. POST `/like` (Like a post)
*   **Request Body:** `{ "postId": "p999" }`
*   **Headers:** `Authorization: Bearer <JWT_TOKEN>`
*   **Logic:**
    1.  Check if user already liked this post (prevent duplicates).
    2.  If not → insert like document in MongoDB.
    3.  Increment `likes_count` on the post (via Redis first, then sync to DB).
*   **Response:** `200 OK` → `{ "liked": true, "totalLikes": 1401 }`

#### 6. POST `/follow` (Follow a user)
*   **Request Body:** `{ "targetUserId": 205 }`
*   **Headers:** `Authorization: Bearer <JWT_TOKEN>`
*   **Logic:**
    1.  Check if already following (SQL query).
    2.  If not → insert row into SQL `followers` table.
    3.  Increment `followers_count` for target user and `following_count` for current user.
    4.  Re-build the current user's feed to include the new person's posts.
*   **Response:** `200 OK` → `{ "following": true }`
*   **Error:** `409 Conflict` → `{ "error": "Already following this user" }`

---

### 🚀 Deep Dive: Backend Logic (Express.js)

In a real production system, the backend is organized into **Layers**. This keeps the code clean and easy to fix.

#### 1. The Route Layer (The Waiter)
This is the entry point. It defines the URL.
```javascript
// routes/postRoutes.js
router.post('/create-post', authMiddleware, upload.single('photo'), postController.createPost);
```

#### 2. The Middleware Layer (The Security Guard)
Before reaching the logic, the request must pass "Checks."
*   **Auth Middleware:** Decodes the **JWT Token** to see who you are.
*   **Upload Middleware (Multer):** Handles the incoming high-speed file data from your phone.

#### 3. The Controller Layer (The Kitchen Manager)
This is where the actual logic lives. It coordinates between the database and the services.
```javascript
// controllers/postController.js
const createPost = async (req, res) => {
    const photo = req.file; // The original huge file
    const caption = req.body.caption;

    // 1. Call a Service to shrink the photo
    const optimizedPhotoUrl = await imageService.shrinkAndUpload(photo);

    // 2. Save to Database
    const newPost = await Post.create({
        userId: req.user.id,
        imageUrl: optimizedPhotoUrl,
        caption: caption
    });

    res.status(201).json(newPost);
};
```

---

### 🖼️ File Upload & Image Shrinking Logic

When you upload an 8MB photo, we don't just save it. We **process** it to save space and speed.

#### **How "Shrinking" Works In-Depth:**
1.  **Buffering:** The server receives the 8MB file in "chunks" (small pieces) and stores it in temporary memory.
2.  **Resizing (Sharp Library):** We use a Node.js library called **Sharp**. It reads the pixel data and "discards" extra pixels to change a 4000x4000 image into a 1080x1080 image.
3.  **Compression:** We lower the "quality" from 100% to 80%. *Human eyes can't see the difference, but the file size drops by 70%!*
4.  **Formatting:** We convert heavy `.png` files into modern `.webp` or `.jpg` formats.
5.  **Uploading Versions:** We don't just upload one. We upload:
    *   `thumb_post123.jpg` (Small)
    *   `standard_post123.jpg` (Medium)
    *   `original_post123.jpg` (High Res)

#### **Why do this in the Backend?**
*   **Consistency:** If we let the phone do it, every brand of phone might do it differently.
*   **Security:** We can check if the file is secretly a "virus" before saving it.
*   **Power:** Servers are much more powerful at mathematical shrinking than a budget smartphone.

---

### Feed Generation Logic (The "News Feed" Secret)

Generating a feed for millions of people is the most expensive part of Instagram. There are two main ways to do it, and Instagram uses a clever mix of both.

#### 1. The Pull Model (The Library Search)
*   **Analogy:** Imagine you want to read news. You go to the library, search through 100 different newspapers, find the stories you like, and then sit down to read.
*   **How it works:** When you open the app, the server says: *"Wait! Let me check who you follow... okay, now let me search the Database for all their latest posts... okay, now let me sort them by time."*
*   **Pros:** Very easy for the server when people *post* something.
*   **Cons:** Very **slow** for you when you *open* the app, because the server has to do a lot of work every single time you refresh.

#### 2. The Push Model (The Pizza Delivery)
*   **Analogy:** You tell the pizza shop your favorite toppings once. Every time a new pizza is ready, they deliver it directly to your door. When you're hungry, it’s already there!
*   **How it works:** When your friend uploads a photo, the server immediately "pushes" a copy of that photo into a special "Pre-built Feed" (Cache/Redis) for every single follower.
*   **Pros:** Lightning-fast! When you open the app, the feed is already built and waiting for you.
*   **Cons:** Very hard for the server if the person has millions of followers.

#### ⚡ The "Celebrity Problem" (Why Push fails for stars)
Imagine **Cristiano Ronaldo** posts a photo. He has **600 Million followers**.
*   If we use the **Push Model**, the server has to make **600 million copies** of that post and put them into 600 million different mailboxes instantly.
*   This would **crash the entire system** and take hours to finish. 

#### 🚀 The Instagram Solution: The Hybrid Model
Instagram uses a "Smart Mix":
1.  **For Normal Users (Like you and me):** They use the **Push Model**. Since we only have a few hundred followers, pushing to them is fast and keeps the app smooth.
2.  **For Celebrities (The Stars):** They use the **Pull Model**. When Ronaldo posts, the system does **nothing** for his followers.
3.  **The Magic Trick:** When *you* open your app, Instagram's backend does two things:
    *   It grabs your pre-built feed (from people like your friends).
    *   It quickly "pulls" the latest posts from any celebrities you follow.
    *   It merges them together and shows them to you in milliseconds!

---

### 🛠️ Code Implementation: Push vs Pull (Express.js)

Understanding how this works in code will make you a much better developer. Here is how we build these models using **Node.js** and **Redis**.

#### 1. The Push Model (Fan-out on Write)
When a user with 500 followers posts a photo, the server "pushes" it into 500 different "mailboxes" in **Redis**.

```javascript
// postController.js
const createPost = async (req, res) => {
    // 1. Save the post to the main Database (MongoDB)
    const newPost = await Post.create(req.body);

    // 2. Find all followers of this user (SQL)
    const followers = await Follower.findAll({ where: { followingId: req.user.id } });

    // 3. PUSH to every follower's mailbox (Redis Cache)
    followers.forEach(follower => {
        // We push the Post ID into a Redis "List" for each follower
        // This is called "Fan-out"
        redis.lpush(`feed:${follower.id}`, newPost.id);
        redis.ltrim(`feed:${follower.id}`, 0, 499); // Keep only the latest 500 posts
    });

    res.status(201).json({ message: "Post pushed to followers!" });
};
```

#### 2. The Pull Model (Fan-out on Load)
When you open your app, you "pull" the feed from everyone you follow. This is usually for people following celebrities.

```javascript
// feedController.js
const getPullFeed = async (req, res) => {
    // 1. Who does this user follow?
    const followingIds = await Follower.findAll({ where: { followerId: req.user.id } });

    // 2. SEARCH the database for the newest posts from those people
    const feed = await Post.find({
        user_id: { $in: followingIds }
    }).sort({ createdAt: -1 }).limit(20);

    res.json(feed);
};
```

#### 3. The Hybrid Model (The Final Boss)
This is what a real system like Instagram uses. It checks the "Mailbox" (Push) and also checks for "Celebrity Posts" (Pull).

```javascript
// feedController.js
const getHybridFeed = async (req, res) => {
    const userId = req.user.id;

    // STEP A: Get the "Pre-built" feed from Redis (Push Model results)
    const pushedPostIds = await redis.lrange(`feed:${userId}`, 0, 19);

    // STEP B: Find which celebrities the user follows
    const celebrities = await Follower.findAll({ 
        where: { followerId: userId, isCelebrity: true } 
    });

    // STEP C: Pull the latest posts from those Celebrities
    const celebPosts = await Post.find({
        user_id: { $in: celebrities.map(c => c.id) }
    }).limit(10);

    // STEP D: Merge them and Sort by Time
    const finalFeed = [...pushedPostIds, ...celebPosts].sort((a, b) => b.time - a.time);

    res.json(finalFeed);
};
```

#### **Why is this better?**
*   **Speed:** You get your friends' posts in 0.001 seconds from Redis.
*   **Cost:** You only search the slow database for a few celebrities, not for 1,000 friends.
*   **Scale:** Ronaldo can post as much as he wants, and the server won't crash!

---

## Scalability (VERY IMPORTANT)

Scalability = The system's ability to handle MORE users without slowing down.

Instagram has **2 billion+ users**. You can't run that on one computer. Here's how we scale:

---

### 1. Horizontal Scaling
**What:** Instead of making one computer bigger (vertical), we add MORE computers (horizontal).

**Analogy:** Imagine a restaurant with 1 chef. If 100 orders come in, you don't buy a bigger stove — you hire 10 more chefs.

```text
Vertical Scaling:           Horizontal Scaling:
┌──────────────┐           ┌────────┐ ┌────────┐ ┌────────┐
│  1 BIG       │           │ Small  │ │ Small  │ │ Small  │
│  Server      │    vs     │ Server │ │ Server │ │ Server │
│  ($10,000)   │           │ ($500) │ │ ($500) │ │ ($500) │
└──────────────┘           └────────┘ └────────┘ └────────┘
(Has a limit!)              (Add more as needed!)
```

**How in Instagram:**
- We run 100+ Node.js backend instances behind a Load Balancer.
- If traffic spikes (e.g., New Year's Eve), we auto-add more servers (Auto-scaling with AWS EC2).
- When traffic drops, we remove servers to save money.

---

### 2. Load Balancing
**What:** A traffic controller that spreads incoming requests across multiple servers.

**Why:** Without it, Server #1 gets 10 million requests and crashes, while Servers #2-#100 sit idle.

**How it Works:**
```text
1 Million Users
      ↓
[ Load Balancer ] (e.g., AWS ALB / Nginx)
   ↓      ↓      ↓
Server1  Server2  Server3
(333K)   (333K)   (333K)    ← Evenly distributed!
```

**Algorithms used:**
| Algorithm | How it Works | Best For |
|:---|:---|:---|
| **Round Robin** | Request 1 → Server A, Request 2 → Server B, Request 3 → Server C, repeat | Equal server specs |
| **Least Connections** | Send to the server with fewest active requests | Varying request times |
| **IP Hash** | Same user always goes to the same server | Session-based apps |

---

### 3. Caching (Redis)

**What:** A super-fast storage layer (in RAM) between your backend and database.

**Why:** Database reads take **5-50ms**. Redis reads take **0.1ms**. That's 50-500x faster.

**What to Cache:**
| Data | Cache Duration | Why |
|:---|:---|:---|
| User feed | 5 minutes | Feed doesn't change every second |
| User profile | 1 hour | Name/bio rarely changes |
| Post likes count | 30 seconds | Counts change often but don't need to be exact |
| Session/JWT data | 24 hours | Avoids hitting DB on every API call |

**Cache Flow (Cache-Aside Pattern):**
```text
User asks for Feed
    ↓
Is feed in Redis? ── YES → Return from Redis (0.1ms) ✅
    ↓ NO
Query MongoDB for feed (50ms)
    ↓
Save result in Redis with TTL (Time To Live)
    ↓
Return to user
```

```javascript
// Redis caching example in Node.js
const getFeed = async (req, res) => {
    const userId = req.user.id;
    const cacheKey = `feed:${userId}`;

    // Step 1: Check Redis first
    const cachedFeed = await redis.get(cacheKey);
    if (cachedFeed) {
        return res.json(JSON.parse(cachedFeed)); // Cache HIT ✅
    }

    // Step 2: Cache MISS — query the database
    const feed = await Post.find({ /* ... */ }).sort({ createdAt: -1 }).limit(20);

    // Step 3: Save to Redis for 5 minutes (300 seconds)
    await redis.setex(cacheKey, 300, JSON.stringify(feed));

    res.json(feed);
};
```

---

### 4. CDN (Content Delivery Network)

**What:** A network of servers spread across the world that stores COPIES of your images/videos.

**Why:** If a user in India requests an image stored on a server in the USA, the data has to travel 15,000 km. With a CDN, the image is cached on a server in Mumbai — 0 km travel!

```text
Without CDN:                  With CDN (AWS CloudFront):
User (India) ──15,000km──→   User (India) ──100km──→ CDN Edge (Mumbai)
    USA Server                     ↓ (If not cached)
    (Slow! 500ms)                 USA Server (Origin)
                                  (Fast! 20ms)
```

**How Instagram uses CDN:**
1. User uploads photo → stored in S3 (USA origin).
2. First user in India requests photo → CDN fetches from S3, caches it in Mumbai.
3. Next 1 million users in India → served from Mumbai cache (instant!).

---

### 5. Database Scaling

**Read Replicas:**
```text
Write requests → Primary DB (1 server)
Read requests  → Replica DB (5+ servers)

Why? 90% of Instagram traffic is READING (viewing feeds, profiles).
     Only 10% is WRITING (posting, liking).
     We create copies of the database just for reading.
```

**Sharding (Splitting the Database):**
```text
Instead of 1 database with 2 billion users:

Shard 1: Users A-F (400M users)
Shard 2: Users G-L (400M users)
Shard 3: Users M-R (400M users)
Shard 4: Users S-Z (400M users)

Each shard is on a different server → No single server is overloaded!
```

**Sharding Strategies:**
| Strategy | How | Example |
|:---|:---|:---|
| **Range-based** | Split by ID range | Users 1-1M → Shard 1, 1M-2M → Shard 2 |
| **Hash-based** | Hash the user ID, route to shard | hash(userId) % 4 → Shard 0, 1, 2, or 3 |
| **Geo-based** | Split by region | India users → Shard India, USA → Shard USA |

---

## Performance Optimization

*   **Pagination:** Don't load 1,000 posts at once. Load 20, then load more as the user scrolls (Infinite Scroll using cursor-based pagination).
*   **Lazy Loading:** Only download the image when it's about to appear on the screen.
*   **Indexing:** Create database indexes on `UserID`, `email`, `post_id` so lookups take 0.001s instead of 10s.
*   **Connection Pooling:** Keep a "pool" of database connections ready instead of creating new ones per request.
*   **Compression:** Gzip API responses to reduce data transferred by 70%.
*   **WebSockets:** For real-time features (like "typing..." in DMs), use persistent connections instead of polling.

---

## Deep Dive Topics (VERY IMPORTANT)

### 1. Load Balancer — Deep Dive

**What:** A server that distributes traffic evenly across multiple backend servers.

**Why:** Without it, one server gets all traffic and crashes while others sit idle.

**Types:**
| Type | Layer | What it Checks |
|:---|:---|:---|
| **L4 (Transport)** | TCP/UDP level | IP address + Port (fast, no content inspection) |
| **L7 (Application)** | HTTP level | URL path, headers, cookies (smart routing) |

**Real-World:** AWS ALB (Application Load Balancer) is L7. It routes `/api/feed` to Feed servers and `/api/upload` to Upload servers.

**Health Checks:** The LB pings each server every few seconds. If a server doesn't respond, it's removed from rotation. When it recovers, it's added back.

**Pros:** Prevents overload, enables zero-downtime deployments, automatic failover.
**Cons:** Adds slight latency, can be a bottleneck if undersized.

---

### 2. API Gateway — Deep Dive

**What:** A single entry point for ALL client requests, sitting before backend services.

**What it Does:**
1. **Authentication:** Validates JWT before requests reach the backend.
2. **Rate Limiting:** Blocks users making too many requests (e.g., 100 req/min).
3. **Request Routing:** Routes `/feed` to Feed Service, `/upload` to Upload Service.
4. **Response Caching:** Caches common responses to reduce backend load.
5. **Logging & Monitoring:** Logs every request for debugging.

**Real-World:** AWS API Gateway or Kong. Instagram handles billions of requests/day through their gateway.

**Pros:** Single security layer, easy monitoring, simplifies client code.
**Cons:** Single point of failure (solved with redundancy), adds slight latency.

---

### 3. Caching — Deep Dive

**When to cache vs when NOT to:**

| Cache ✅ | Don't Cache ❌ |
|:---|:---|
| Data that rarely changes (profiles) | Data that changes every second |
| Data accessed by many users (trending posts) | Sensitive data (passwords) |
| Expensive DB queries (feed) | Data that MUST be 100% accurate (bank balance) |

**Cache Invalidation:**
```javascript
// When a user updates their profile — delete stale cache:
const updateProfile = async (req, res) => {
    await User.update(req.user.id, req.body);
    await redis.del(`user:${req.user.id}`); // Invalidate cache
    // Next read will fetch fresh data from DB and re-cache it
};
```

**Eviction Policies:**
- **LRU (Least Recently Used):** Remove the item not accessed for the longest time.
- **TTL (Time To Live):** Each item expires after a set duration (e.g., 5 minutes).

---

### 4. Feed Generation — Deep Dive

**The complete pipeline:**
```text
Step 1: User opens Instagram → GET /feed
Step 2: Check Redis for pre-built feed (Push model results)
Step 3: Fetch celebrity posts from MongoDB (Pull model)
Step 4: Apply ranking algorithm (not just time-based!)
Step 5: Filter out posts user already saw
Step 6: Add advertisements (every 5th post)
Step 7: Return paginated results (20 posts)
```

**Ranking Algorithm (Why your feed isn't just "newest first"):**
```text
Post Score = (Recency × 0.3) + (Relationship × 0.3) + (Engagement × 0.2) + (ContentType × 0.2)

- Recency: How new is the post?
- Relationship: How often do you interact with this person?
- Engagement: How many likes/comments does this post have?
- ContentType: Do you prefer photos or videos?
```

---

### 5. Database Scaling — Deep Dive

**Problem:** One PostgreSQL server handles ~10K queries/s. Instagram needs ~1M queries/s.

**Solution Stack:**
1. **Connection Pooling** (PgBouncer) → Efficient connection sharing.
2. **Read Replicas** → 5-10 read-only copies for read-heavy traffic.
3. **Caching** (Redis) → Reduce 80% of DB reads.
4. **Sharding** → Split data across servers.
5. **Archiving** → Move old data to cold storage.

```javascript
// MongoDB sharding example:
sh.shardCollection("instagram.posts", { "user_id": "hashed" });
// Posts auto-distributed across shards by user_id hash
```

---

## Tech Stack Usage

| Technology | Role | Why We Chose It |
|:---|:---|:---|
| **Next.js** | Frontend | SSR for fast loads, SEO-friendly, built-in routing |
| **Node.js** | Backend runtime | Non-blocking I/O, handles thousands of concurrent connections |
| **Express.js** | Backend framework | Lightweight, flexible, huge middleware ecosystem |
| **PostgreSQL** | SQL Database | ACID compliance, powerful JOINs for user/follow data |
| **MongoDB** | NoSQL Database | Flexible schema, horizontal scaling for posts/comments |
| **Redis** | Cache | Sub-millisecond reads, pub/sub, feed storage |
| **AWS S3** | Object Storage | Unlimited storage, 99.999999999% durability |
| **AWS CloudFront** | CDN | 400+ edge locations, integrates with S3 |
| **AWS EC2** | Compute | Auto-scaling, pay-per-use |
| **Docker** | Containers | Consistent deployments across all environments |
| **Nginx** | Load Balancer | High-performance reverse proxy |

**How they connect (MERN Stack + AWS):**
```text
User → CloudFront (CDN) → Nginx (LB) → Express.js (Node.js)
                                            ↓
                                   Redis (Cache) ←→ PostgreSQL (Users/Follows)
                                            ↓
                                   MongoDB (Posts/Comments)
                                            ↓
                                   S3 (Image/Video files)
```

---

## Real-World Flow Example: Uploading a Post

```text
1. User taps "Share" on their phone (Next.js frontend)
2. Load Balancer routes request to available backend server
3. API Gateway validates JWT token (is this user authenticated?)
4. Express.js backend receives the photo + caption
5. Multer middleware handles the file stream
6. Sharp library resizes → creates thumb, standard, and original
7. All 3 versions uploaded to AWS S3 → S3 returns URLs
8. Post metadata saved to MongoDB (URLs, caption, userId, timestamp)
9. Background Worker starts fan-out:
   → Finds all followers from PostgreSQL
   → Pushes post ID into each follower's Redis feed list
10. CDN caches images at edge locations worldwide
11. Followers open app → feed from Redis → images from CDN
12. Post appears on screen in <200ms! ✅
```

---

## Trade-offs

### 1. SQL vs MongoDB
| Aspect | SQL (PostgreSQL) | MongoDB |
|:---|:---|:---|
| **Strength** | Data integrity, JOINs, ACID | Flexible schema, horizontal scaling |
| **Weakness** | Hard to scale horizontally | Weaker consistency guarantees |
| **Use Case** | Users, Followers | Posts, Comments |

**Decision:** Use **both** — "Polyglot Persistence."

### 2. Push vs Pull for Feed
| Aspect | Push (Fan-out on Write) | Pull (Fan-out on Read) |
|:---|:---|:---|
| **Write Cost** | High | Low |
| **Read Cost** | Low (pre-built) | High (search on read) |
| **Best For** | <10K followers | Millions of followers |

**Decision:** **Hybrid** — Push for normal users, Pull for celebrities.

### 3. Embedded vs Referenced Documents
| Aspect | Embedded | Referenced |
|:---|:---|:---|
| **Read Speed** | Faster (one query) | Slower (two queries) |
| **Data Size** | 16MB limit | No limit |

**Decision:** Embed small data (replies). Reference large data (comments separate from posts).

---

## Practical Tasks

### Task 1: Design Story Feature
**Challenge:** Stories disappear after 24 hours. How would you design this?

**Hint Solution:**
- Store stories in MongoDB with a `created_at` field.
- Use MongoDB's **TTL Index** — it auto-deletes documents after a set time.
```javascript
// Auto-delete stories after 24 hours (86400 seconds)
db.stories.createIndex({ "created_at": 1 }, { expireAfterSeconds: 86400 });
```
- Keep active stories in Redis for fast reads.
- Store story views in a separate collection for analytics.

### Task 2: Add Notification System
**Challenge:** Notify users when someone likes their post or follows them.

**Hint Solution:**
- Use a **Message Queue** (RabbitMQ or AWS SQS).
- When a like happens → push a message to the queue.
- A **Notification Worker** reads the queue and:
  - Saves notification to MongoDB.
  - Sends push notification via Firebase Cloud Messaging.
  - Updates the unread count in Redis.

### Task 3: Improve Feed Performance
**Challenge:** A user follows 5,000 people. Feed is slow.

**Hint Solution:**
1. Pre-build the feed using Push model (store in Redis).
2. Use cursor-based pagination (not offset-based).
3. Only fetch post metadata first, lazy-load images.
4. Cache the top 500 posts per user with a 5-minute TTL.
5. Use read replicas for database queries.

### Task 4: Design Direct Messaging (DMs)
**Challenge:** How to build real-time chat?

**Hint Solution:**
- Use **WebSockets** (Socket.io) for real-time delivery.
- Store messages in MongoDB.
- Use Redis Pub/Sub for cross-server message routing.
- Show "typing..." indicator via WebSocket events.

---

## Interview Questions

**Q1: How would you design the Instagram feed?**
*   **A:** Use a Hybrid approach. Push (Fan-out on write) for regular users and Pull (Fan-out on load) for celebrities. On read, merge pre-built feed from Redis with pulled celebrity posts, apply a ranking algorithm, and paginate.

**Q2: How to scale image uploads?**
*   **A:** Use AWS S3 for storage and CDN for delivery. Offload image processing (resize, compress) to background workers using a job queue so users don't wait. Use pre-signed URLs for direct client-to-S3 uploads for large files.

**Q3: Why is a CDN used in Instagram?**
*   **A:** To reduce latency by serving media from edge servers close to users. Without CDN, an Indian user waits 500ms+ for a US image. With CDN, it's under 20ms from a local edge.

**Q4: SQL vs NoSQL for Instagram?**
*   **A:** SQL (PostgreSQL) for structured relational data like Users and Followers — it guarantees ACID and supports JOINs. NoSQL (MongoDB) for high-volume flexible data like Posts and Comments — it scales horizontally and handles variable documents well.

**Q5: How to handle millions of concurrent users?**
*   **A:** Horizontal scaling with auto-scaling (AWS EC2), Load Balancers for distribution, Redis caching to reduce DB load by 80%+, CDN for static assets, read replicas, and database sharding.

**Q6: How would you design the "Like" system?**
*   **A:** Use eventual consistency. Increment count in Redis instantly (UI responsiveness), then async update MongoDB in background. Store individual likes in a separate collection to support "unlike" and "check if liked."

**Q7: What is "Sharding" in databases?**
*   **A:** Breaking one giant database into smaller pieces (shards) across servers. Example: `hash(userId) % 4` routes users to one of 4 shard servers, distributing load evenly.

**Q8: How do you prevent duplicate posts in feed?**
*   **A:** Maintain "Seen Post IDs" set in Redis per session. Use cursor-based pagination (pass `last_seen_post_id`) instead of offset-based to avoid duplicates from new inserts.

**Q9: What happens if S3 goes down?**
*   **A:** Use Multi-Region replication (S3 Cross-Region Replication). Photos auto-copied to different regions. If one fails, CDN serves from another. S3 has 99.999999999% (11 nines) durability.

**Q10: What is Rate Limiting and why?**
*   **A:** Caps requests per user per time window (e.g., 100 API calls/min). Prevents bots, spam, and DDoS attacks. Implemented at API Gateway using Token Bucket or Sliding Window algorithms.

**Q11: How does the "Explore" page work?**
*   **A:** Recommendation engine tracks what content you engage with (likes, watch time, followed hashtags), then uses collaborative filtering ("Users similar to you also liked..."). Results are pre-computed and cached in Redis.

**Q12: How to handle a celebrity posting during a viral event?**
*   **A:** This is the "Thundering Herd" problem. Never use Push for celebrities. Queue celebrity post processing with rate limiting. Pre-warm CDN caches for the media. Use auto-scaling to add servers during predicted spikes.

**Q13: How to ensure consistency between SQL and MongoDB?**
*   **A:** Use the Saga Pattern for cross-database operations — execute as a sequence with compensating transactions if any step fails. For simpler cases, use eventual consistency with background sync jobs.

**Q14: Horizontal vs Vertical scaling?**
*   **A:** Vertical = bigger server (more RAM, CPU). Simpler but has a physical limit. Horizontal = more servers with load distribution. More complex but no theoretical limit. Instagram uses horizontal.

**Q15: How would you design the search feature?**
*   **A:** Use Elasticsearch for full-text search. Index usernames, hashtags, locations. Implement autocomplete with prefix matching. Cache popular searches in Redis. Rank by relevance (followers, engagement).

---

> **Study Tip:** Don't try to memorize diagrams. Understand **WHY** each piece exists (Redis = speed, S3 = files, SQL = relationships, MongoDB = content). Interviewers want to see you **reason** about trade-offs, not recite answers!

