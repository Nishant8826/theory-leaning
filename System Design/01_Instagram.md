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

---

## Architecture Diagram (Text Based)

```text
[ User's Phone ] 
       ↓
[ Load Balancer ] (Spreads the traffic)
       ↓
[ API Gateway ] (Security & Routing)
       ↓
[ Backend (Express.js) ] ↔ [ Cache (Redis) ] (For fast speed)
       ↓           ↘
[ Database ]       [ Storage (AWS S3) ] (For Photos/Videos)
(SQL & NoSQL)              ↓
                     [ CDN ] (Fast delivery to users)
```

---

## Database Design

### Why use BOTH SQL & MongoDB?
*   **SQL (PostgreSQL/MySQL):** Best for data that needs strict rules. For example, "User A follows User B" is a clear relationship. You don't want a "ghost follow" where one side disappears.
*   **NoSQL (MongoDB):** Best for "messy" data. Posts can have different sizes, different numbers of tags, and millions of comments. NoSQL handles this "heavy" data faster.

### Schema Examples

**SQL (Relational) - Users Table**
| UserID | Username | Email | Password_Hash |
| :--- | :--- | :--- | :--- |
| 101 | nishant_dev | n@test.com | $2b$10... |

**SQL (Relational) - Followers Table**
| FollowerID | FollowingID | Created_At |
| :--- | :--- | :--- |
| 101 | 205 | 2024-01-01 |

**MongoDB (NoSQL) - Posts Collection**
```json
{
  "post_id": "p999",
  "user_id": 101,
  "image_url": "https://s3.aws.com/my-photo.jpg",
  "caption": "Living my best life! #dev",
  "likes_count": 1400,
  "comments": [
    {"user": "rahul", "text": "Cool pic!"},
    {"user": "amit", "text": "Where is this?"}
  ]
}
```

---

## Low-Level Design (LLD)

### API Design (The Conversation)
As we discussed, APIs are like conversations between your phone and the server. In our **Express.js** backend, we define "Routes" for these conversations.

#### 1. POST `/create-post` (Uploading your content)
*   **What happens?** Your phone sends the photo and caption.
*   **Request Body:** `FormData` containing the Image and `caption`.
*   **Logic (Mental Model):**
    1.  **Auth Check:** Is the user logged in? (Middleware).
    2.  **File Validation:** Is it an image? Is it too big?
    3.  **Process:** Shrink the photo for fast loading (Detailed below).
    4.  **Save:** Put file in S3 → Put link in MongoDB.
*   **Response:** `201 Created` with the new Post ID.

#### 2. GET `/feed` (Getting your timeline)
*   **What happens?** The phone asks for the latest posts.
*   **Request Params:** `page` (starts at 1) and `limit` (e.g., 20 posts).
*   **Logic:**
    1.  Consult SQL database: *"Who does this user follow?"*
    2.  Consult MongoDB: *"Get 20 latest posts from those Followed IDs."*
    3.  Sort by `timestamp`.
*   **Response:** `200 OK` with an array of objects.

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

### Authentication
*   We use **JWT (JSON Web Tokens)**. 
*   When you login, the server gives you a "Digital Key" (Token).
*   Your phone saves this key. Every time you want to "Like" or "Post," you show this key to the server so it knows it’s really you.

---

## Scalability

*   **Horizontal Scaling:** Instead of buying one giant expensive computer, we use 1,000 cheap ones. If traffic grows, we add 1,001.
*   **Load Balancing:** Ensuring no single server is "sweating" while others are "sleeping."
*   **Caching (Redis):** If 1 million people are looking at the same celebrity photo, we don't ask the database 1 million times. We save it in a "Super Fast Memory" called **Redis** and serve it from there.
*   **CDN:** Moving data closer to the user’s physical city.

---

## Performance Optimization

*   **Pagination:** Don't load 1,000 posts at once. Load 10, then load more as the user scrolls (Infinite Scroll).
*   **Lazy Loading:** Only download the image when it’s about to appear on the screen.
*   **Indexing:** In the database, we create a "Table of Contents" (Index) for `UserID` so searching for a user’s posts takes 0.001s instead of 10 seconds.

---

## Tech Stack (Summary)

*   **Next.js:** For a fast, SEO-friendly frontend.
*   **Node.js:** For a fast, non-blocking backend that handles many users at once.
*   **SQL (PostgreSQL):** For secure and reliable "Follow" and "User" data.
*   **MongoDB:** For storing heavy global data like Posts and Comments.
*   **AWS S3:** For safe and cheap image/video storage.
*   **AWS CloudFront (CDN):** To make the app fast everywhere in the world.
*   **Docker:** To pack our app so it runs exactly the same on any server.
*   **Redis:** For lightning-fast caching.

---

## Real-World Flow Example: Uploading a Post

1.  **User** clicks "Share."
2.  **API Gateway** checks if the user is a real person (Security).
3.  **Backend** takes the photo, shrinks the size, and sends it to **AWS S3**.
4.  **S3** gives back a link (`s3.com/my-pic.jpg`).
5.  **Backend** saves this link + caption into **MongoDB**.
6.  **Background Worker** starts "pushing" this post into the feeds of the user's followers.
7.  **Followers** see the new post on their screen!

---

## Trade-offs

### 1. SQL vs MongoDB
*   **Trade-off:** SQL is hard to scale but very safe. MongoDB is easy to scale but can lose data if not handled carefully.
*   **Decision:** We use **both** to get the best of both worlds!

### 2. Push vs Pull for Feed
*   **Trade-off:** Push is fast for users but heavy for the server. Pull is slow for users but light for the server.
*   **Decision:** Use **Hybrid**. Push for small users, Pull for big celebrities.

---

## Practical Tasks

1.  **Design Story Feature:** Imagine Instagram Stories (posts that disappear in 24 hours). How would you change the database to handle the "24-hour" rule? (Hint: TTL Index in MongoDB).
2.  **Add Notification System:** How would you notify a user when someone likes their post? (Hint: Use a Message Queue like RabbitMQ).
3.  **Improve Feed Performance:** If a user follows 5,000 people, the feed is slow. How would you use **Redis** to make it faster?

---

## Interview Questions

**Q1: How would you design the Instagram feed?**
*   **A:** Use a Hybrid approach. Push (Fan-out on write) for regular users and Pull (Fan-out on load) for high-profile celebrities to balance speed and system load.

**Q2: How to scale image uploads?**
*   **A:** Use an Object Storage like AWS S3 and a CDN (Content Delivery Network). Offload the processing (resizing) to background workers so the user doesn't have to wait.

**Q3: Why is a CDN used in Instagram?**
*   **A:** To reduce "latency." It serves images from a server physically close to the user, making the app feel significantly faster.

**Q4: SQL vs NoSQL for Instagram?**
*   **A:** Use SQL for structured data like User Profiles and Followers (Relationships). Use NoSQL (MongoDB/Cassandra) for high-volume data like Posts, Likes, and Comments.

**Q5: How to handle millions of concurrent users?**
*   **A:** Use Horizontal Scaling, Load Balancers to distribute traffic, and Caching (Redis) to reduce database hits.

**Q6: How would you design the "Like" system?**
*   **A:** Use an "eventual consistency" model. Update the count in a fast cache (Redis) first, then slowly update the main database in the background.

**Q7: What is "Sharding" in databases?**
*   **A:** It’s breaking one giant database table into smaller pieces (shards) and spreading them across multiple servers so no single server gets overloaded.

**Q8: How do you prevent a user from seeing the same post twice in their feed?**
*   **A:** Store a "Seen Post IDs" list for the user session (in Redis) and filter them out during feed generation.

**Q9: What happens if the S3 storage is down?**
*   **A:** This is why we use Multi-Region storage. We keep copies of the photos in different geographical places so if one goes down, the others work.

**Q10: What is Rate Limiting and why do we need it?**
*   **A:** It limits how many actions a user can take (e.g., 60 likes per minute) to prevent bots and spam from crashing our servers.

---

> **Study Tip:** Don't try to memorize the diagram. Try to understand **WHY** we added each piece (e.g., Redis is for speed, S3 is for big files). That is what interviewers look for!
