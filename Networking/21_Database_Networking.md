# Database Networking

> 📌 **File:** 21_Database_Networking.md | **Level:** Full-Stack Dev → Networking Expert

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
│  PostgreSQL │ PostgreSQL     │ 5432  │ TCP + TLS (RDS)          │
│  MySQL      │ MySQL Protocol │ 3306  │ TCP + TLS (RDS)          │
│  Redis      │ RESP           │ 6379  │ TCP (+ TLS for ElastiCache)│
│  DynamoDB   │ HTTPS (REST)   │ 443   │ Standard HTTP/TLS        │
└────────────────┴────────────────┴───────┴──────────────────────────┘
```

---

## Connection Pooling (The Most Important Concept)

```
Without pool (new connection per query):
  Query 1: TCP handshake (1.5 RTT) + TLS (1 RTT) + Auth + Query + Close
  Query 2: TCP handshake (1.5 RTT) + TLS (1 RTT) + Auth + Query + Close
  
  3 queries to MongoDB Atlas (cross-region, 50ms RTT):
  Connection overhead: 3 × (75ms + 50ms + 20ms) = 435ms wasted!

With pool (reuse connections):
  Startup: TCP + TLS + Auth (once for each pool connection)
  Query 1: Send command → receive result (50ms)
  Query 2: Send command → receive result (50ms)
  
  3 queries: 150ms total (vs 585ms without pool) — 4x faster!
```

#### Diagram Explanation (The Bouncer List)
Think of Database Connection Pooling like getting into a nightclub:
- **Without a Pool:** Every time you want to order a drink, you have to exit the club, stand in the back of the line outside, show your ID to the bouncer (TCP/TLS Handshake), wait for approval, get your drink, and leave. You waste 400ms just standing in line for a 50ms transaction!
- **With a Pool:** The bouncer checks your ID *once* at the start of the night and gives you a VIP wristband. Now, you can instantly order drinks without having to re-verify your identity! The connection pool keeps a set of "pre-verified VIP" connections open permanently.

### Connection Pool Configuration

```javascript
// MongoDB Connection Pool
const mongoose = require('mongoose');

mongoose.connect(process.env.MONGO_URI, {
  maxPoolSize: 10,
  minPoolSize: 2,
  maxIdleTimeMS: 30000,
  connectTimeoutMS: 10000,
  socketTimeoutMS: 45000,
  keepAlive: true
});

// PostgreSQL Connection Pool
const { Pool } = require('pg');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 10000,
  ssl: {
    rejectUnauthorized: true,
    ca: fs.readFileSync('./rds-combined-ca-bundle.pem')
  }
});
```

---

## Replica and Read Scaling

- **MongoDB Atlas Replica Set:**
  - Primary (us-east-1a): Reads + Writes
  - Secondaries (us-east-1b/c): Reads only (replication lag)
  - If Primary fails, a Secondary becomes Primary automatically.
- **RDS PostgreSQL Read Replicas:**
  - Primary (writer): Writes + critical reads
  - Read Replicas: Read-only (async replication)
  - Writer endpoint: `mydb.cluster-xxxxx.rds.amazonaws.com`
  - Reader endpoint: `mydb.cluster-ro-xxxxx.rds.amazonaws.com`

#### Diagram Explanation (The Head Chef and the Sous Chefs)
To prevent your primary database from melting under pressure, you must implement Read Replicas:
- **The Primary (The Head Chef):** The only one allowed to write new recipes or change core orders (`Writes`).
- **The Replicas (The Sous Chefs):** They constantly copy everything the Head Chef writes down. If customers ask to look at the menu (`Reads`), the Sous Chefs handle those requests so the Head Chef isn't distracted from cooking!

```javascript
// PostgreSQL: Separate reader and writer pools
const writerPool = new Pool({ connectionString: process.env.WRITER_URL });
const readerPool = new Pool({ connectionString: process.env.READER_URL });

async function createOrder(data) {
  return writerPool.query('INSERT INTO orders (data) VALUES ($1) RETURNING *', [data]);
}

async function getOrders(userId) {
  return readerPool.query('SELECT * FROM orders WHERE user_id = $1', [userId]);
}
```

---

## Practice Exercises

### Exercise 1: Pool Monitoring
Add pool event logging (connect, disconnect, error) to your MongoDB and PostgreSQL connections. Run load tests and observe pool behavior.

### Exercise 2: Latency Measurement
Measure the latency of a simple ping query. Compare localhost vs MongoDB Atlas. Calculate connection overhead.

---

## Interview Q&A

**Q1: Why is connection pooling important for databases?**
> Each new connection requires a TCP handshake (1.5 RTT), TLS handshake (1-2 RTT), and authentication. A pool creates connections once and reuses them. For cross-region connections at 50ms RTT, this saves 150-250ms per query.

**Q2: How do you handle database connection failures in Node.js?**
> Use connection event handlers (`disconnected`, `error`, `reconnected`) for logging and metrics. Implement health check endpoints that verify DB connectivity. Return 503 to clients when DB is down rather than crashing.

**Q3: What is the connection limit problem and how do you solve it?**
> PostgreSQL: process per connection (limited). MongoDB: tier-based limits. Too many app instances × too many pool connections = exhausted limits. Solutions: right-size pools, use connection proxies (PgBouncer for PostgreSQL).

**Q4: How does database replication affect your application networking?**
> Writes go to primary, reads can go to replicas. Replication is async — replicas may be slightly behind (lag). For read-after-write consistency, read from primary immediately after a write.

**Q5: What is the NAT Gateway timeout problem for database connections?**
> AWS NAT Gateway drops idle TCP connections after 350 seconds. If connection pool has idle connections longer than 350s, NAT silently drops them. Fix: set TCP keep-alive interval < 350s on database connections.

---

Prev : [20 Kubernetes Networking](./20_Kubernetes_Networking.md) | Index: [00 Index](./00_Index.md) | Next : [22 VPC Architecture And Design](./22_VPC_Architecture_And_Design.md)
