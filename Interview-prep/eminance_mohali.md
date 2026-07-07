# Eminence Mohali Technical Interview Prep Guide


### ❓ Q1. What roadmap would you follow to optimize an API that takes 45–50 seconds to respond, exceeding a 30-second timeout?
<details>
<summary><b>👀 Show Answer</b></summary>

An API taking 45-50 seconds is a major bottleneck, often caused by inefficient database queries, blocking operations, network latency, or synchronous processing of heavy tasks. The optimized roadmap should be divided into phases:

#### Phase 1: Immediate Mitigation & Architecture Shift (Short Term)
1. **Convert Synchronous to Asynchronous Processing (Job Queues):**
   * If the API does heavy tasks (e.g., PDF generation, video encoding, batch data crunching), it should **not** run synchronously within the HTTP request-response cycle.
   * **Solution:** Return an immediate `202 Accepted` status with a unique job ID. Offload the heavy task to a background queue system (like **BullMQ** with **Redis**, or **RabbitMQ**).
   * The client can poll a status endpoint (`GET /api/jobs/:id`) or receive a push notification via WebSockets or webhooks when the processing is complete.
2. **Implement Caching (Redis):**
   * For read-heavy endpoints, introduce a caching layer using Redis. 
   * Bypass the database entirely for identical requests within a specified TTL (Time-To-Live).

#### Phase 2: Diagnostics & Profiling
1. **APM & Query Profiling:**
   * Use Application Performance Monitoring (APM) tools (e.g., Datadog, New Relic) to find the exact line of code or SQL query causing the latency.
   * Run database-level tools: Use SQL's `EXPLAIN` or `EXPLAIN ANALYZE` on database queries to inspect their execution plans. Identify if there are sequential scans, missing indexes, or expensive sorts.

#### Phase 3: Query & Database-Level Optimizations
1. **Avoid `SELECT *`:**
   * Selecting all columns increases disk I/O, network overhead, and memory usage. Explicitly fetch only the columns required.
2. **Optimize Joins:**
   *   **Index Foreign Keys:** Every column used in a `JOIN` condition (e.g., `ON users.id = orders.user_id`) **must** be indexed on both sides. Joining tables on unindexed columns forces the database engine to perform slow **full table scans** for every single comparison.
   *   **Avoid the N+1 Query Problem (Select-in-Loop):** 
       *   *The Problem:* Fetching a list of 100 orders, and then running a separate query in a loop to fetch the customer details for each order (`100 + 1 = 101` database round trips).
       *   *The Solution:* Use a single `INNER JOIN` or `LEFT JOIN` query (or Sequelize `include` / Mongoose `populate`) to fetch all orders and their customer details in **one single database call**.
   *   **Select Only Needed Columns:** Avoid `SELECT *` across joined tables. If you join `users` with `orders` and `profiles`, specify exactly which columns you need (e.g. `SELECT users.username, orders.total`). This minimizes network payload transfer and database memory usage.
   *   **Filter Before Joining (Early Filtering):** Apply filter conditions (`WHERE` clauses) as early as possible so that the database engine joins only the matching subset of rows instead of joining the entire tables first and filtering them afterwards.
   *   **Use Subqueries / Common Table Expressions (CTEs) for Aggregates:** If you need to join a table to calculate aggregate statistics (e.g. counting the number of comments per post), calculate the counts in a subquery or CTE first, and then perform the join on the aggregated results to avoid large, temporary join tables.
3. **Indexing:**
   * Add B-Tree indexes on fields frequently used in `WHERE`, `ORDER BY`, or `JOIN` clauses.
   * Use **Composite Indexes** for queries filtering on multiple columns (e.g., `WHERE status = 'active' AND created_at > ...`). *Note: Always respect the leftmost prefix rule.*
4. **Use Stored Procedures (Where Appropriate):**
   * Stored procedures execute directly on the database engine. By wrapping multiple query steps in a single stored procedure, you eliminate network round trips between the application server and the database server.
5. **Database Connection Pooling:**
   * Ensure the application reuses connections instead of establishing a new connection on every single request.

#### Phase 4: Database Scale Out
* Read/Write splitting (send write operations to the primary DB instance, and read operations to read-replicas).

</details>

---


### ❓ Q2. How do you implement IP-based rate limiting with a rolling time window (e.g., 15 minutes) in Node.js, and how do you use the express-rate-limit package?
<details>
<summary><b>👀 Show Answer</b></summary>

Here is the correct way to implement rate limiting both from scratch (using an in-memory global object) and using the standard production library `express-rate-limit`.

---

#### 1. Custom In-Memory Implementation (Correct Way)
To implement a true **rolling (sliding) window**, we must track individual request timestamps instead of a simple counter. Using a global object, we store an array of timestamps (in milliseconds) for each IP. When a new request arrives, we prune timestamps older than the 15-minute window before counting.

```javascript
// Global store mapping IP addresses to arrays of request timestamps
const requestHistory = {}; 

const rateLimiter = (req, res, next) => {
  try {
    const userIp = req.ip;
    const now = Date.now();
    const WINDOW_MS = 15 * 60 * 1000; // 15 minutes rolling window
    const DEFAULT_LIMIT = 100;        // Max requests allowed per window

    // Initialize the history array if the IP is seen for the first time
    if (!requestHistory[userIp]) {
      requestHistory[userIp] = [];
    }

    // 1. Prune timestamps that fall outside the 15-minute rolling window
    const cutoffTime = now - WINDOW_MS;
    requestHistory[userIp] = requestHistory[userIp].filter(timestamp => timestamp > cutoffTime);

    // 2. Check if request count exceeds the limit
    if (requestHistory[userIp].length >= DEFAULT_LIMIT) {
      return res.status(429).send({ message: "Too many requests. Please try again later." });
    }

    // 3. Record the current request timestamp and proceed
    requestHistory[userIp].push(now);
    next();
    
  } catch (error) {
    // Fail-safe: Always call next() on failure to avoid locking users out if code crashes
    next(); 
  }
};

// 4. Memory Cleanup: Periodically delete inactive IPs to prevent memory leaks
setInterval(() => {
  const now = Date.now();
  const WINDOW_MS = 15 * 60 * 1000;
  for (const ip in requestHistory) {
    requestHistory[ip] = requestHistory[ip].filter(timestamp => timestamp > now - WINDOW_MS);
    if (requestHistory[ip].length === 0) {
      delete requestHistory[ip];
    }
  }
}, 5 * 60 * 1000); // Runs every 5 minutes
```

---

#### 2. Production-Grade Rate Limiting with `express-rate-limit`
In production, instead of writing custom rate limiters from scratch, developers use `express-rate-limit`, the standard package for rate limiting in Express apps.

**Installation:**
```bash
npm install express-rate-limit
```

**Basic Usage:**
```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per `windowMs`
  message: { message: "Too many requests. Please try again later." },
  standardHeaders: true, // Return standard rate limit info headers (RateLimit-Limit, RateLimit-Remaining)
  legacyHeaders: false, // Disable the deprecated X-RateLimit-* headers
});

// Apply the rate limiting middleware to all API requests
app.use('/api/', limiter);
```

#### How `express-rate-limit` Works and Scales:
*   **Memory Management:** By default, it uses an in-memory store (`MemoryStore`) to keep track of hits. It automatically cleans up memory without needing manual `setInterval` definitions.
*   **Scaling Horizontally:** The default `MemoryStore` does not work across multiple server instances (e.g., behind a load balancer), and state is reset on server restarts. 
*   **Redis Integration:** To resolve this, you can configure `express-rate-limit` to use an external database like **Redis** for state storage by plugging in `rate-limit-redis`:
    ```javascript
    const rateLimit = require('express-rate-limit');
    const RedisStore = require('rate-limit-redis');
    const Redis = require('ioredis');

    const redisClient = new Redis();

    const limiter = rateLimit({
      windowMs: 15 * 60 * 1000,
      max: 100,
      // Store state in Redis instead of server RAM
      store: new RedisStore({
        sendCommand: (...args) => redisClient.call(...args),
      }),
    });
    ```

</details>

---


### ❓ Q3. What is the basic difference between a Virtual Machine (VM) and a Docker container?
<details>
<summary><b>👀 Show Answer</b></summary>

The fundamental difference lies in their **architecture** and the level at which they **virtualize resources**.

| Feature | Virtual Machine (VM) | Docker Container |
| :--- | :--- | :--- |
| **Virtualization Level** | **Hardware-level virtualization**. Virtualizes physical hardware via a Hypervisor (e.g., VMware ESXi, Hyper-V, KVM). | **OS-level virtualization**. Virtualizes the Operating System, sharing the host OS kernel. |
| **Guest OS** | **Required**. Each VM must run a full Guest OS (including its own kernel, system libraries, and drivers). | **No Guest OS**. Shares the Host OS kernel. Contains only libraries and application binaries. |
| **Isolation** | Strong security isolation since each VM operates on virtualized hardware independently. | Process-level isolation using Linux kernel features (`namespaces` and `cgroups`). Slightly weaker isolation than VMs. |
| **Resource Overhead** | High. Consumes gigabytes of RAM/disk for the guest OS alone. | Low. Shares host resources; filesystems are highly compressed. Typically megabytes in size. |
| **Startup Time** | Slow (minutes), as it must boot a complete operating system. | Near-instant (milliseconds to seconds), as it only launches the app process. |
| **Portability** | Harder to migrate due to VM size and dependency on hypervisor formats (OVF, VMDK). | Extremely portable. "Build once, run anywhere" as long as a Docker daemon is present. |

#### Architectural Diagram:
```text
+-----------------------+      +-----------------------+
|  App 1  |   App 2     |      |  App 1  |   App 2     |
+---------+-------------+      +---------+-------------+
| Guest OS|  Guest OS   |      |   Docker Engine       |
+---------+-------------+      +-----------------------+
|      Hypervisor       |      |       Host OS         |
+-----------------------+      +-----------------------+
|      Host OS / HW     |      |      Bare Metal / HW  |
+-----------------------+      +-----------------------+
|     VIRTUAL MACHINE   |      |        CONTAINER      |
+-----------------------+      +-----------------------+
```

</details>

---


### ❓ Q4. Can you write a CI/CD pipeline configuration (using GitHub Actions and Jenkinsfile) to deploy a React Web / Mobile application and walk through it?
<details>
<summary><b>👀 Show Answer</b></summary>

Here are syntax-correct workflows for **GitHub Actions** (React Web and React Native) and **Jenkins** (React Web).

---

### Option A: React Web Deployment using GitHub Actions (AWS S3 + CloudFront)
Create this file under `.github/workflows/deploy-react-web.yml`:

```yaml
name: Production Deployment (React Web)

# Trigger the workflow on pushes to the main branch
on:
  push:
    branches:
      - main

# Define the sequence of jobs to run
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      # Step 1: Checkout the source code
      - name: Checkout Repository
        uses: actions/checkout@v4

      # Step 2: Set up Node.js with caching to speed up builds
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      # Step 3: Install exact dependencies using package-lock.json
      - name: Install Dependencies
        run: npm ci

      # Step 4: Run test suite
      - name: Run Tests
        run: npm test -- --watchAll=false

      # Step 5: Build production assets with injected Environment Variables
      - name: Build Project
        run: npm run build
        env:
          REACT_APP_API_URL: ${{ secrets.REACT_APP_API_URL }}

      # Step 6: Configure AWS credentials
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      # Step 7: Sync the build output folder to the S3 bucket
      - name: Deploy to S3
        run: aws s3 sync dist/ s3://${{ secrets.AWS_S3_BUCKET_NAME }} --delete

      # Step 8: Invalidate CloudFront CDN cache to reflect new changes immediately
      - name: Invalidate CloudFront Cache
        run: aws cloudfront create-invalidation --distribution-id ${{ secrets.AWS_CLOUDFRONT_DISTRIBUTION_ID }} --paths "/*"
```

---

### Option B: React Native / Expo Mobile App Build (Using EAS CLI)
Create this file under `.github/workflows/build-react-native.yml`:

```yaml
name: Build Mobile App (React Native via Expo)

on:
  push:
    tags:
      - 'v*' # Trigger build on release tags, e.g. v1.2.0

jobs:
  build-mobile:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      # Setup Expo integration and CLI
      - name: Setup Expo
        uses: expo/expo-github-action@v8
        with:
          expo-version: latest
          token: ${{ secrets.EXPO_TOKEN }} # EAS Token from Expo account secrets

      - name: Install Dependencies
        run: npm ci

      # Trigger Expo Application Services (EAS) cloud builds for Android and iOS
      - name: EAS Build Production
        run: eas build --platform all --profile production --local=false --non-interactive
```

---

### Option C: React Web Deployment using Jenkins (Declarative Jenkinsfile)
Create this file under `Jenkinsfile` in the project root:

```groovy
// Jenkinsfile - Defines the deployment pipeline executed by the Jenkins Server
pipeline {
    agent any // Executes the build on any available worker node
    
    environment {
        AWS_ACCESS_KEY_ID     = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
        S3_BUCKET             = 's3://my-react-production-bucket'
        CLOUDFRONT_DIST_ID    = 'E1A2B3C4D5E6F7'
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Checkout code from Git SCM configured in Jenkins job settings
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                // Install dependencies exactly matching package-lock.json
                sh 'npm ci'
            }
        }
        
        stage('Run Tests') {
            steps {
                // Run tests in non-interactive watch-free mode
                sh 'npm test -- --watchAll=false'
            }
        }
        
        stage('Build') {
            steps {
                // Compile React production build assets to dist/
                sh 'npm run build'
            }
        }
        
        stage('Deploy to AWS S3') {
            steps {
                // Sync dist/ build assets with S3 bucket and delete removed assets
                sh "aws s3 sync dist/ ${S3_BUCKET} --delete"
            }
        }
        
        stage('Invalidate CloudFront Cache') {
            steps {
                // Clear CDN cache index so edge servers load new index.html immediately
                sh "aws cloudfront create-invalidation --distribution-id ${CLOUDFRONT_DIST_ID} --paths '/*'"
            }
        }
    }
    
    post {
        success {
            echo 'MERN application deployed successfully!'
        }
        failure {
            echo 'Build failed. Check execution console logs.'
        }
    }
}
```

---

#### Pipeline Walkthrough & Mechanics:

1.  **Triggers:**
    *   **GitHub Actions:** Uses `on: push` configurations (triggers on branches like `main` or specific tags like `v*`).
    *   **Jenkins:** Typically triggered via **Git Webhooks** (GitHub pushes trigger a push notification to `/github-webhook/` on the Jenkins server) or **SCM Polling**.
2.  **Environment Credentials Security:**
    *   **GitHub Actions:** Uses `${{ secrets.NAME }}` loaded from GitHub Repo Secrets settings.
    *   **Jenkins:** Uses the `credentials()` helper, mapping secure credentials stored in the Jenkins Global Credentials Store directly to pipeline environment variables securely.
3.  **Deployment Steps (S3 + CloudFront):**
    *   **`aws s3 sync --delete`:** Minimizes updates by comparing hashes and uploading only changed files, and deletes deleted files from the S3 bucket.
    *   **`aws cloudfront create-invalidation`:** Invalidates the cache on CloudFront edge nodes (specifically `index.html`) so users download the new build index script immediately, bypassing old cache entries.

> 💡 **Interviewer Focus:** Pipeline configuration syntax, securing secrets in build environments, optimizing build caching, and understanding the role of CloudFront cache invalidations post-S3 deployment.

</details>

---


### ❓ Q5. What is the difference between database sharding and database partitioning, and when do we use each?
<details>
<summary><b>👀 Show Answer</b></summary>

Here is the direct comparison between database partitioning and sharding:

---

#### 1. Direct Explanation

*   **Database Partitioning (Table-Level Scaling)**
    *   **What it is:** Splitting a single massive table into smaller physical segments (called partitions) **within the same database server**.
    *   **How it works:** The database engine (e.g., MySQL, PostgreSQL) automatically routes queries to the correct partition based on a key (like a date range or category).
    *   **Primary Goal:** To speed up query performance on massive tables by reducing index sizes and scanning only target partitions instead of the whole table.

*   **Database Sharding (Database/Server-Level Scaling)**
    *   **What it is:** Distributing a database's records across **multiple separate database servers (instances)**.
    *   **How it works:** The dataset is split horizontally (e.g., users with IDs 0-1M go to Server A, IDs 1M-2M go to Server B). The application layer or a routing middleware directs database operations to the correct server.
    *   **Primary Goal:** To scale write throughput, memory consumption, connections, and storage capacity when a single server hits its hardware limits.

---

#### 2. Key Differences at a Glance

| Feature | Partitioning (Table-Level) | Sharding (Database/Server-Level) |
| :--- | :--- | :--- |
| **Physical Location** | All data remains on a **single database server**. | Data is spread across **multiple physical servers**. |
| **Management** | Managed entirely by the database engine (transparent to the app). | Managed at the application layer or via routing middleware (Vitess, Citus). |
| **Complexity** | Low. Standard SQL queries work out-of-the-box. | High. Multi-server queries, joins, and transaction management are complex. |
| **When to use** | When a single table's index becomes too slow to scan, but the server has ample resources. | When a single server runs out of storage, RAM, CPU, or concurrent connection limits. |

---

#### 3. Real-World Industry Examples & Code Snippets

##### Example A: Table-Level Partitioning (E-Commerce Order Logs)
*Scenario:* An e-commerce platform has a single database server running PostgreSQL. The `orders` table has 500 million rows, making historical data scans slow.
*Solution:* Partition the `orders` table by **Range** using the `order_date` field. The database engine dynamically splits data into yearly tables.

```sql
-- 1. Create a parent partitioned table specifying the partition key
CREATE TABLE orders (
    order_id INT NOT NULL,
    user_id INT NOT NULL,
    order_date DATE NOT NULL,
    amount DECIMAL(10, 2),
    PRIMARY KEY (order_id, order_date)
) PARTITION BY RANGE (order_date);

-- 2. Create actual child partition tables that hold the physical records
CREATE TABLE orders_2025 PARTITION OF orders
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

CREATE TABLE orders_2026 PARTITION OF orders
    FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

-- 3. The application inserts data into the parent table
INSERT INTO orders (order_id, user_id, order_date, amount) 
VALUES (99901, 2030, '2025-06-15', 150.00);
-- Behind the scenes, the PostgreSQL engine transparently writes this record 
-- directly to the physical 'orders_2025' table.
```

##### Example B: Server-Level Sharding (Multi-Region SaaS Application)
*Scenario:* A SaaS app has clients worldwide. The total database load exceeds the CPU and connection limit of a single server.
*Solution:* Shard the database horizontally by **Geographical Region** (Shard Key). US users are routed to the US server, European users to the EU server.

```javascript
const mysql = require('mysql2/promise');

// 1. Configure separate connection pools pointing to completely different physical server nodes
const shards = {
  shard_us: mysql.createPool({ host: 'db-us-east.company.com', user: 'app_user', database: 'prod_db' }),
  shard_eu: mysql.createPool({ host: 'db-eu-west.company.com', user: 'app_user', database: 'prod_db' }),
  shard_ap: mysql.createPool({ host: 'db-ap-south.company.com', user: 'app_user', database: 'prod_db' })
};

// 2. Application router chooses the appropriate connection pool (machine) based on the Shard Key
async function getUserOrderDetails(userId, userRegion) {
  let selectedPool;

  switch(userRegion.toLowerCase()) {
    case 'us':
      selectedPool = shards.shard_us;
      break;
    case 'eu':
      selectedPool = shards.shard_eu;
      break;
    default:
      selectedPool = shards.shard_ap; // Fallback to Asia-Pacific node
  }

  // 3. Query executes on the chosen physical server instance
  const [rows] = await selectedPool.query('SELECT * FROM orders WHERE user_id = ?', [userId]);
  return rows;
}
```

</details>

---


### ❓ Q6. Which React hook runs first, and how do React functional hooks map to class-based lifecycle methods?
<details>
<summary><b>👀 Show Answer</b></summary>

#### Which Hook Runs First?
Among the side-effect hooks in React, **`useInsertionEffect` runs first**, followed by **`useLayoutEffect`**, and finally **`useEffect`**.

Here is the exact execution lifecycle in React 18:
1.  **Render Phase:** The functional component runs. React evaluates the JSX and computes the virtual DOM diff.
2.  **`useInsertionEffect` (Pre-DOM Mutations):** Introduced in React 18 for CSS-in-JS libraries. It fires synchronously *before* React mutates the actual DOM, allowing dynamic `<style>` tags to be injected.
3.  **DOM Mutation:** React updates the real DOM nodes.
4.  **`useLayoutEffect` (Post-DOM Mutation, Pre-Paint):** Fires synchronously *after* DOM mutations but *before the browser paints* the screen. This allows you to read layout dimensions and make DOM alterations synchronously to prevent visual flickering.
5.  **Paint Phase:** The browser draws the layout pixels on the screen.
6.  **`useEffect` (Post-Paint):** Fires asynchronously *after* the paint phase. This ensures that heavy side-effects (like APIs or event listeners) do not block visual rendering.

---

#### Mapping Class-Based Lifecycles to Functional Hooks:
Functional components do not have lifecycle methods; instead, they synchronize side-effects with state and props using hooks.

| Class Lifecycle Method | Hook Equivalent in Functional Components | Key Difference / Detail |
| :--- | :--- | :--- |
| **`componentDidMount`** | ```javascript useEffect(() => { /* mount code */ }, []) ``` | Runs exactly once after the initial render. |
| **`componentDidUpdate`** | ```javascript useEffect(() => { /* update code */ }, [count]) ``` | **Note:** Unlike `componentDidUpdate` (which *only* runs on updates), `useEffect` also fires on the initial mount. To replicate `componentDidUpdate` exactly, you must use a `useRef` to skip the first execution. |
| **`componentWillUnmount`** | ```javascript useEffect(() => { return () => { /* cleanup */ } }, []) ``` | The returned cleanup function runs when the component is unmounting. |
| **`shouldComponentUpdate`** | Wrapped in **`React.memo()`** | Bypasses re-rendering the component if its props did not change (performs a shallow comparison). |

##### **Pro-Tip: Replicating `componentDidUpdate` Exactly (Skipping Mount)**
If you want a hook to run only on state changes and *never* on the initial render:
```javascript
import { useEffect, useRef } from 'react';

function useCustomEffect(callback, dependencies) {
  const isFirstRender = useRef(true);

  useEffect(() => {
    if (isFirstRender.current) {
      isFirstRender.current = false;
      return; // Skip the first execution (mount)
    }
    return callback();
  }, dependencies);
}
```

</details>

---


### ❓ Q7. What are the roles of useMemo, useCallback, and React.memo in React memoization?
<details>
<summary><b>👀 Show Answer</b></summary>

Memoization is an optimization technique used to prevent unnecessary computations and re-renders by caching outputs. React provides three primary tools:

#### 1. `useMemo`
*   **Purpose:** Caches the **returned value** of an expensive function.
*   **Mechanism:** Runs the function only when dependency array items change. If they remain the same, it returns the cached result.
*   **Example:**
    ```javascript
    const expensiveCalculation = (num) => {
      // Simulate high CPU computation
      for (let i = 0; i < 1000000000; i++) {}
      return num * 2;
    };

    function MyComponent({ count }) {
      const doubled = useMemo(() => expensiveCalculation(count), [count]);
      return <div>Doubled: {doubled}</div>;
    }
    ```

#### 2. `useCallback`
*   **Purpose:** Caches the **function definition/reference** itself.
*   **Mechanism:** React recreates functional declarations on every single render. When passing callbacks to child components, a new reference triggers child re-renders. `useCallback` keeps the same reference until dependencies change.
*   **Example:**
    ```javascript
    function ParentComponent() {
      const [count, setCount] = useState(0);

      // Prevents reference change on every Parent re-render
      const handleIncrement = useCallback(() => {
        setCount(prev => prev + 1);
      }, []); // Dependency array

      return <ChildComponent onIncrement={handleIncrement} />;
    }
    ```

#### 3. `React.memo`
*   **Purpose:** A **Higher-Order Component (HOC)** that prevents an entire component from re-rendering if its props haven't changed.
*   **Mechanism:** Performs a shallow comparison of props. If props are unchanged, React skips re-rendering the component and reuses the last rendered result.
*   **Example:**
    ```javascript
    const ChildComponent = React.memo(function Child({ onIncrement }) {
      console.log("Child rendered!");
      return <button onClick={onIncrement}>Increment</button>;
    });
    ```

</details>

---


### ❓ Q8. How can sockets be scaled in a real-time chat application?
<details>
<summary><b>👀 Show Answer</b></summary>

Scaling real-time socket connections (like WebSockets) involves handling persistent connections, data processing latency, and state synchronization across multiple instances.

#### 1. Payload Chunking and Server-Side Buffering
*   **Problem:** Sending large payloads at once blocks the node process thread (due to CPU-heavy JSON serialization/deserialization) and spikes memory consumption.
*   **Solution:** Stream data in smaller chunks. 
*   Implement a server-side buffer that queues incoming chunks, concatenates them, and processes/persists them asynchronously using database batching rather than writing on every small packet.

#### 2. Horizontal Scaling with Redis Pub/Sub (Adapter pattern)
*   **Problem:** If User A is connected to Socket Server Instance 1, and User B is connected to Socket Server Instance 2, they cannot communicate because they exist on different server memory stacks.
*   **Solution:** Introduce a Redis Pub/Sub backplane (e.g., using `@socket.io/redis-adapter`).
*   When Server 1 receives a message, it publishes it to a Redis channel. All other server instances (2, 3, etc.) subscribe to that channel, receive the message, and emit it to User B if they are connected on their instance.

```text
+----------+             +-----------------+             +----------+
|  User A  | ===(WS)===> | Socket Server 1 |             | Socket   |
+----------+             +-----------------+             | Server 2 |
                                || (Publish)             +----------+
                                \/                           ||
                       +-----------------+                   || (Emit WS)
                       | Redis Pub/Sub   | ===(Broadcast)==> ||
                       +-----------------+                   \/
                                                         +----------+
                                                         |  User B  |
                                                         +----------+
```

#### 3. Load Balancing with Sticky Sessions
*   **Problem:** A WebSocket connection starts with an HTTP Handshake (upgrade request). If a standard Round-Robin load balancer routes the upgrade handshake to a different server instance than the initial HTTP polling attempt, the connection will fail.
*   **Solution:** Configure the load balancer (Nginx, AWS Application Load Balancer) to use **Sticky Sessions (Session Affinity)**, ensuring a client always hits the same server instance during handshakes and reconnects.

#### 4. Distributed State Management (Tracking Online Users)
*   **Problem:** Storing active user states (e.g., "who is online") in the application memory of Server 1 makes it inaccessible to Server 2, preventing features like real-time user online indicators.
*   **Solution:** Store active connection metadata in a centralized **Redis** database (e.g., using a Redis Set or Hash). When a client connects, the handling server registers their status in Redis; when they disconnect, the record is removed. Any backend instance can check Redis to verify user presence.

#### 5. System-Level Tune-ups
*   **Increase File Descriptor Limits (`ulimit`):** By default, Linux OS limits open file descriptors (connections are treated as files). Raise this limit (e.g., to 65535 or higher) on host machines.

</details>

---


### ❓ Q9. How do you set up a Redux store using Redux Toolkit (RTK) vs legacy Redux?
<details>
<summary><b>👀 Show Answer</b></summary>

**Redux Toolkit (RTK)** is the modern standard for writing Redux logic. It eliminates boilerplate, configures the store with standard defaults, and uses the **Immer** library under the hood to allow writing "mutable" state update logic safely.

---

### Option A: Modern Redux Toolkit (RTK) Setup (Recommended)

#### Step 1: Create a Slice (`features/counterSlice.js`)
```javascript
import { createSlice } from '@reduxjs/toolkit';

const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: (state) => {
      // Immer allows us to "mutate" state directly
      state.value += 1;
    },
    decrement: (state) => {
      state.value -= 1;
    },
    incrementByAmount: (state, action) => {
      state.value += action.payload;
    }
  }
});

export const { increment, decrement, incrementByAmount } = counterSlice.actions;
export default counterSlice.reducer;
```

#### Step 2: Configure the Store (`app/store.js`)
```javascript
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from '../features/counterSlice';

export const store = configureStore({
  reducer: {
    counter: counterReducer
  }
});
```

#### Step 3: Wrap App with Provider (`index.js`)
```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { store } from './app/store';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <Provider store={store}>
    <App />
  </Provider>
);
```

#### Step 4: Access State and Dispatch Actions in Component (`App.js`)
```javascript
import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { increment, decrement } from './features/counterSlice';

export default function App() {
  const count = useSelector((state) => state.counter.value);
  const dispatch = useDispatch();

  return (
    <div>
      <h1>Count: {count}</h1>
      <button onClick={() => dispatch(increment())}>Increment</button>
      <button onClick={() => dispatch(decrement())}>Decrement</button>
    </div>
  );
}
```

---

### Option B: Legacy Redux Setup (For Reference)

In legacy Redux, you have to write action creators, action types, and manual non-mutating reducers (using spread operators).

#### Step 1: Define Actions (`store/actions.js`)
```javascript
// Action Types
export const INCREMENT = 'INCREMENT';
export const DECREMENT = 'DECREMENT';

// Action Creators
export const increment = () => ({ type: INCREMENT });
export const decrement = () => ({ type: DECREMENT });
```

#### Step 2: Define Reducer (`store/reducer.js`)
```javascript
import { INCREMENT, DECREMENT } from './actions';

const initialState = { value: 0 };

export default function counterReducer(state = initialState, action) {
  switch (action.type) {
    case INCREMENT:
      // Must manually return a new state object to avoid mutations
      return { ...state, value: state.value + 1 };
    case DECREMENT:
      return { ...state, value: state.value - 1 };
    default:
      return state;
  }
}
```

#### Step 3: Create Store (`store/store.js`)
```javascript
import { createStore } from 'redux';
import counterReducer from './reducer';

const store = createStore(counterReducer);
export default store;
```

</details>

---

## 📝 Notes & Interview Summary

*   **Interview Feedback:** The interviewer concluded the session without any follow-ups and provided positive oral feedback, indicating the session was complete and satisfactory.
*   **Resolved Open Items:**
    *   **Rate Limiting Timing Mechanics:** Detailed the in-memory rolling window mechanism using a global object tracking arrays of timestamps, and compared it with a production-grade Redis Sorted Set (`zset`) approach.
    *   **CI/CD Pipeline Configurations:** Provided syntax-complete CI/CD workflows for both React Web deployment (using GitHub Actions and declarative Jenkinsfile to S3/CloudFront) and React Native builds (via Expo/EAS CLI).

