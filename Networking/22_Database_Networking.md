# Database Networking

> 📌 **File:** 22_Database_Networking.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

Every database query is a network operation — TCP connection, authentication, query transmission, result transfer. Understanding database networking explains why connection pools exist, why cross-region queries are slow, why replica lag happens, and how to diagnose "can't connect to database" issues.

---

## Map it to MY STACK (CRITICAL)

```
┌──────────────────────────────────────────────────────────────────┐
│  Database   │ Protocol       │ Port  │ Connection Type          │
├─────────────┼────────────────┼───────┼──────────────────────────┤
│  MongoDB    │ MongoDB Wire   │ 27017 │ TCP + TLS (Atlas)        │
│             │ Protocol       │       │ Persistent connection pool│
│             │                │       │                          │
│  PostgreSQL │ PostgreSQL     │ 5432  │ TCP + TLS (RDS)          │
│  (RDS)      │ Protocol       │       │ Process per connection   │
│             │                │       │                          │
│  MySQL      │ MySQL Protocol │ 3306  │ TCP + TLS (RDS)          │
│             │                │       │ Thread per connection    │
│             │                │       │                          │
│  Redis      │ RESP           │ 6379  │ TCP (+ TLS for Elasti)  │
│             │ (text-based)   │       │ Single-threaded, pipelined│
│             │                │       │                          │
│  DynamoDB   │ HTTPS (REST)   │ 443   │ Standard HTTP/TLS        │
│             │                │       │ No connection pool needed│
└─────────────┴────────────────┴───────┴──────────────────────────┘
```

---

## Connection Pooling (The Most Important Concept)

```
Without pool (new connection per query):
  Query 1: TCP handshake (1.5 RTT) + TLS (1 RTT) + Auth + Query + Close
  Query 2: TCP handshake (1.5 RTT) + TLS (1 RTT) + Auth + Query + Close
  Query 3: TCP handshake (1.5 RTT) + TLS (1 RTT) + Auth + Query + Close
  
  3 queries to MongoDB Atlas (cross-region, 50ms RTT):
  Connection overhead: 3 × (75ms + 50ms + 20ms) = 435ms wasted!

With pool (reuse connections):
  Startup: TCP + TLS + Auth (once for each pool connection)
  Query 1: Send command → receive result (50ms)
  Query 2: Send command → receive result (50ms)
  Query 3: Send command → receive result (50ms)
  
  3 queries: 150ms total (vs 585ms without pool) — 4x faster!
```

### Connection Pool Configuration

```javascript
// ──── MongoDB Connection Pool ────
const mongoose = require('mongoose');

mongoose.connect(process.env.MONGO_URI, {
  // Pool settings
  maxPoolSize: 10,        // Max connections in pool (default: 100 — too many!)
  minPoolSize: 2,         // Keep 2 warm connections
  maxIdleTimeMS: 30000,   // Close idle connections after 30s
  
  // Timeout settings
  connectTimeoutMS: 10000,    // Initial connection timeout
  socketTimeoutMS: 45000,     // Query timeout
  serverSelectionTimeoutMS: 30000, // How long to find a server
  heartbeatFrequencyMS: 10000,    // Check server health every 10s
  
  // Keep-alive (prevent NAT timeout)
  keepAlive: true,
  keepAliveInitialDelay: 120000,  // 120s < NAT Gateway 350s timeout
  
  // Retry
  retryWrites: true,
  retryReads: true,
  
  // TLS (Atlas requires it)
  tls: true
});

// Monitor pool events
mongoose.connection.on('connected', () => console.log('MongoDB connected'));
mongoose.connection.on('disconnected', () => console.log('MongoDB disconnected'));
mongoose.connection.on('error', (err) => console.error('MongoDB error:', err));

// ──── PostgreSQL Connection Pool ────
const { Pool } = require('pg');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,                  // Max connections (RDS default max: 100-500)
  idleTimeoutMillis: 30000, // Close idle connections after 30s
  connectionTimeoutMillis: 10000, // Timeout waiting for available connection
  
  // TLS for RDS
  ssl: {
    rejectUnauthorized: true,
    ca: fs.readFileSync('./rds-combined-ca-bundle.pem')
  }
});

pool.on('connect', () => console.log('New PG client connected'));
pool.on('error', (err) => console.error('PG pool error:', err));

// Proper query pattern
async function query(text, params) {
  const client = await pool.connect();  // Get connection from pool
  try {
    const result = await client.query(text, params);
    return result.rows;
  } finally {
    client.release();  // ALWAYS release back to pool!
  }
}

// ──── Redis Connection ────
const Redis = require('ioredis');

const redis = new Redis(process.env.REDIS_URL, {
  maxRetriesPerRequest: 3,
  retryStrategy: (times) => Math.min(times * 50, 2000), // Exponential backoff
  lazyConnect: true,         // Don't connect until first command
  keepAlive: 120000,         // TCP keep-alive every 120s
  connectTimeout: 10000,
  commandTimeout: 5000,
  
  // TLS for ElastiCache
  tls: process.env.REDIS_TLS === 'true' ? {} : undefined,
  
  // Reconnect on error
  reconnectOnError: (err) => {
    return err.message.includes('READONLY'); // Reconnect if failover happened
  }
});
```

---

## Replica and Read Scaling

```
MongoDB Atlas Replica Set:
┌────────────────────────────────────────────────────────┐
│  Primary (us-east-1a)    │ Reads + Writes             │
│  Secondary (us-east-1b)  │ Reads only (replication lag)│
│  Secondary (us-east-1c)  │ Reads only (replication lag)│
├────────────────────────────────────────────────────────┤
│  Node.js reads from secondary = lower primary load    │
│  Replication lag: typically < 1 second                 │
│  If primary fails → secondary becomes primary (auto)  │
└────────────────────────────────────────────────────────┘

RDS PostgreSQL Read Replicas:
┌────────────────────────────────────────────────────────┐
│  Primary (writer)        │ Writes + critical reads     │
│  Read Replica 1          │ Read-only (async replication)│
│  Read Replica 2          │ Read-only                   │
├────────────────────────────────────────────────────────┤
│  Separate endpoints:                                   │
│  Writer: mydb.cluster-xxxxx.rds.amazonaws.com          │
│  Reader: mydb.cluster-ro-xxxxx.rds.amazonaws.com       │
│  Use reader endpoint for dashboards, reports, search  │
└────────────────────────────────────────────────────────┘
```

```javascript
// ──── MongoDB: Read from secondary for non-critical reads ────
const analytics = await Order.aggregate([
  { $group: { _id: '$status', count: { $sum: 1 } } }
]).read('secondaryPreferred');  // Read from secondary if available

// ──── PostgreSQL: Separate reader and writer pools ────
const writerPool = new Pool({ connectionString: process.env.WRITER_URL });
const readerPool = new Pool({ connectionString: process.env.READER_URL });

// Writes always to primary
async function createOrder(data) {
  return writerPool.query('INSERT INTO orders (data) VALUES ($1) RETURNING *', [data]);
}

// Reads from replica (slightly stale, but reduces primary load)
async function getOrders(userId) {
  return readerPool.query('SELECT * FROM orders WHERE user_id = $1', [userId]);
}
```

---

## Diagnosing Database Connection Issues

```javascript
// ──── Comprehensive connection diagnostics ────
async function diagnoseDBConnections() {
  console.log('=== Database Connection Diagnostics ===\n');
  
  // MongoDB
  try {
    const start = Date.now();
    await mongoose.connection.db.admin().ping();
    console.log(`  MongoDB: ✅ Connected (${Date.now() - start}ms)`);
    console.log(`    Pool: ${mongoose.connection.client.topology?.s?.pool?.size || 'N/A'} connections`);
    console.log(`    Host: ${mongoose.connection.host}:${mongoose.connection.port}`);
  } catch (err) {
    console.log(`  MongoDB: ❌ ${err.message}`);
    if (err.message.includes('ECONNREFUSED')) console.log('    → Check: Is MongoDB running? Security group?');
    if (err.message.includes('ENOTFOUND')) console.log('    → Check: DNS resolution? MongoDB Atlas hostname?');
    if (err.message.includes('authentication')) console.log('    → Check: Username/password? IP whitelist in Atlas?');
    if (err.message.includes('ETIMEDOUT')) console.log('    → Check: VPC routing? NAT Gateway? Security group?');
  }
  
  // Redis
  try {
    const start = Date.now();
    const pong = await redis.ping();
    console.log(`  Redis: ✅ ${pong} (${Date.now() - start}ms)`);
    const info = await redis.info('clients');
    console.log(`    Connected clients: ${info.match(/connected_clients:(\d+)/)?.[1]}`);
  } catch (err) {
    console.log(`  Redis: ❌ ${err.message}`);
  }
  
  // PostgreSQL
  try {
    const start = Date.now();
    const result = await pool.query('SELECT NOW()');
    console.log(`  PostgreSQL: ✅ Connected (${Date.now() - start}ms)`);
    console.log(`    Pool: total=${pool.totalCount}, idle=${pool.idleCount}, waiting=${pool.waitingCount}`);
  } catch (err) {
    console.log(`  PostgreSQL: ❌ ${err.message}`);
  }
}

app.get('/debug/db', async (req, res) => {
  await diagnoseDBConnections();
  res.json({ status: 'check console' });
});
```

---

## Common Mistakes

### ❌ Too Many Connections

```javascript
// ❌ 100 connections to MongoDB × 3 Node.js instances = 300 connections
// Atlas M10 cluster max: 500 connections
// You're using 60% of capacity just on pool overhead!

mongoose.connect(uri, { maxPoolSize: 100 }); // Too many!

// ✅ Right-size your pool
// Formula: maxPoolSize = (total_db_connections_limit / number_of_app_instances) × 0.5
// 500 / 3 / 2 ≈ 80 max, but usually 10-20 is enough
mongoose.connect(uri, { maxPoolSize: 10, minPoolSize: 2 });
```

### ❌ Not Handling Connection Loss

```javascript
// ❌ App crashes when DB connection drops
// No error handling on database operations

// ✅ Graceful reconnection
mongoose.connection.on('disconnected', () => {
  console.warn('MongoDB disconnected — Mongoose will auto-reconnect');
});

mongoose.connection.on('error', (err) => {
  console.error('MongoDB connection error:', err);
  // Don't crash — Mongoose handles reconnection automatically
});

// Check connection health in routes
app.use(async (req, res, next) => {
  if (mongoose.connection.readyState !== 1) {
    return res.status(503).json({ error: 'Database unavailable' });
  }
  next();
});
```

### ❌ Cross-Region Database Queries

```
Node.js in us-east-1 → MongoDB Atlas in ap-south-1
RTT: ~200ms per round trip
Every query: 200ms minimum (just network, ignoring processing!)

✅ Keep compute and database in the same region
✅ Use global clusters for multi-region (Atlas Global Clusters)
✅ Cache frequently-read data in same-region Redis
```

---

## Practice Exercises

### Exercise 1: Pool Monitoring
Add pool event logging (connect, disconnect, error, acquire, release) to your MongoDB and PostgreSQL connections. Run load tests and observe pool behavior.

### Exercise 2: Latency Measurement
Measure the latency of a simple `ping` operation to each of your databases. Compare localhost vs Atlas/RDS. Calculate connection overhead.

### Exercise 3: Read Replica
Set up a PostgreSQL read replica on RDS. Configure separate writer and reader pools in your Express app. Verify queries route correctly.

---

## Interview Q&A

**Q1: Why is connection pooling important for databases?**
> Each new connection requires a TCP handshake (1.5 RTT), TLS handshake (1-2 RTT), and authentication. A pool creates connections once and reuses them. For cross-region connections at 50ms RTT, this saves 150-250ms per query. Also prevents overwhelming the database with too many connections.

**Q2: How do you handle database connection failures in Node.js?**
> Mongoose auto-reconnects with configurable retry strategy. Use connection event handlers (disconnected, error, reconnected) for logging. Implement health check endpoints that verify DB connectivity. Return 503 to clients when DB is down rather than crashing.

**Q3: What is the connection limit problem and how do you solve it?**
> PostgreSQL: process per connection (limited to ~500). MongoDB Atlas: tier-based limits. Too many app instances × too many pool connections = exhausted limits. Solutions: right-size pools, use connection proxies (PgBouncer for PostgreSQL), or serverless-friendly drivers.

**Q4: How does database replication affect your application networking?**
> Writes go to primary, reads can go to replicas. Replication is async — replicas may be slightly behind (lag). Read-after-write consistency: after a write, read from primary (not replica). Use separate connection strings for writer and reader endpoints.

**Q5: What is the NAT Gateway timeout problem for database connections?**
> AWS NAT Gateway drops idle TCP connections after 350 seconds. If your database connection pool has idle connections longer than 350s, NAT silently drops them. Next query fails with ECONNRESET. Fix: set TCP keep-alive interval < 350s on all database connections.
