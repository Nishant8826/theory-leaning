# Deployment & Scaling

> 📌 **File:** 21_Deployment_And_Scaling.md | **Level:** SQL Expert → MongoDB

---

## What is it?

Deploying MongoDB in production involves choices between self-hosted and managed (Atlas), replica sets for high availability, sharding for horizontal scaling, security hardening, backup strategies, and monitoring. As an SQL expert, many concepts map directly — but the operational model for scaling is fundamentally different.

---

## SQL Parallel — Think of it like this

```
SQL:                                     MongoDB:
Single server (dev)                    → Standalone mongod (dev only)
Primary + replicas                     → Replica Set (3+ nodes)
Read replicas                          → Secondary reads
Master-slave replication               → Replica Set (automatic failover)
Sharding (Citus, Vitess)              → Native Sharding (built-in)
pg_dump / mysqldump                    → mongodump / mongorestore
Point-in-time recovery                 → Oplog-based PITR
Connection pooling (PgBouncer)         → Driver-level pooling
pgAdmin / MySQL Workbench              → MongoDB Compass / Atlas UI
RDS / Cloud SQL                        → MongoDB Atlas
```

---

## Deployment Options

```
┌──────────────────────────────────────────────────────────────────────┐
│                     Deployment Options                               │
├─────────────────┬──────────────────────────────────────────────────┤
│  Method          │  Details                                         │
├─────────────────┼──────────────────────────────────────────────────┤
│  Standalone      │  Single mongod. Dev/test only. No redundancy.   │
│  Replica Set     │  3+ nodes. Auto-failover. Production minimum.   │
│  Sharded Cluster │  Replica sets + shards. Horizontal scaling.     │
│  MongoDB Atlas   │  Fully managed. Auto-scaling. Recommended.      │
│  Docker          │  Containerized. Good for dev/staging.           │
│  Kubernetes      │  MongoDB Operator. Enterprise deployments.       │
└─────────────────┴──────────────────────────────────────────────────┘
```

---

## 1. Deploy on EC2 (Ubuntu)

### Install MongoDB

```bash
# Import MongoDB GPG key
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] \
https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Install
sudo apt update
sudo apt install -y mongodb-org

# Start and enable
sudo systemctl start mongod
sudo systemctl enable mongod

# Verify
mongosh --eval "db.adminCommand({ ping: 1 })"
```

### Configure MongoDB

```bash
# Edit configuration
sudo nano /etc/mongod.conf
```

```yaml
# /etc/mongod.conf

storage:
  dbPath: /var/lib/mongodb
  journal:
    enabled: true
  wiredTiger:
    engineConfig:
      cacheSizeGB: 1.5  # ~60% of RAM. 4GB instance → 1.5GB cache
    collectionConfig:
      blockCompressor: snappy  # or zstd for better compression

systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log
  logRotate: rename

net:
  port: 27017
  bindIp: 0.0.0.0  # Allow remote connections (after enabling auth!)
  maxIncomingConnections: 1000

processManagement:
  timeZoneInfo: /usr/share/zoneinfo

# Enable replica set (required for transactions and change streams)
replication:
  replSetName: rs0
  oplogSizeMB: 2048  # 2GB oplog

# Security
security:
  authorization: enabled
  keyFile: /etc/mongodb/keyfile  # For replica set authentication

# Performance
operationProfiling:
  mode: slowOp
  slowOpThresholdMs: 100
```

---

## 2. Secure MongoDB (Auth Enabled)

### Create Admin User

```bash
# Connect without auth (first time only)
mongosh

# Create admin user
use admin
db.createUser({
  user: "admin",
  pwd: "strongAdminPassword123!",
  roles: [
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "readWriteAnyDatabase", db: "admin" },
    { role: "clusterAdmin", db: "admin" }
  ]
})

# Create application user (principle of least privilege)
use ecommerce
db.createUser({
  user: "appuser",
  pwd: "strongAppPassword456!",
  roles: [
    { role: "readWrite", db: "ecommerce" }
  ]
})

# Create read-only user for analytics
db.createUser({
  user: "analyst",
  pwd: "strongAnalystPassword789!",
  roles: [
    { role: "read", db: "ecommerce" }
  ]
})
```

### Enable Authentication

```yaml
# /etc/mongod.conf
security:
  authorization: enabled
```

```bash
# Restart MongoDB
sudo systemctl restart mongod

# Connect with auth
mongosh -u admin -p 'strongAdminPassword123!' --authenticationDatabase admin

# Application connection string
# mongodb://appuser:strongAppPassword456!@ec2-ip:27017/ecommerce?authSource=ecommerce
```

### Security Checklist

```
┌──────────────────────────────────────────────────────────────────┐
│  MongoDB Security Hardening Checklist                            │
├──────────────────────────────────────────────────────────────────┤
│  ✅ Enable authentication (security.authorization: enabled)     │
│  ✅ Create dedicated users per application/role                  │
│  ✅ Use strong passwords (or SCRAM-SHA-256)                     │
│  ✅ Bind to specific IPs (not 0.0.0.0 without firewall)        │
│  ✅ Use TLS/SSL for connections                                  │
│  ✅ Firewall: Only allow port 27017 from app servers            │
│  ✅ Disable unused features (httpInterface, REST)                │
│  ✅ Enable audit logging (Enterprise)                            │
│  ✅ Use VPC/private networking (no public IP)                   │
│  ✅ Keep MongoDB updated (security patches)                     │
│  ✅ Enable encryption at rest (Enterprise or Atlas)             │
├──────────────────────────────────────────────────────────────────┤
│  SQL comparison: Same practices apply to PostgreSQL/MySQL.      │
│  The difference: MongoDB has been historically deployed without │
│  auth, leading to many data breaches. ALWAYS enable auth.       │
└──────────────────────────────────────────────────────────────────┘
```

### AWS Security Group

```
Inbound Rules:
┌──────────┬──────────┬─────────────────────────────────┐
│ Port     │ Protocol │ Source                           │
├──────────┼──────────┼─────────────────────────────────┤
│ 27017    │ TCP      │ App server security group only   │
│ 22       │ TCP      │ Your IP only (for SSH)           │
│ (closed) │ All      │ 0.0.0.0/0 (NEVER open MongoDB)  │
└──────────┴──────────┴─────────────────────────────────┘
```

### TLS/SSL Configuration

```yaml
# /etc/mongod.conf
net:
  tls:
    mode: requireTLS
    certificateKeyFile: /etc/ssl/mongodb.pem
    CAFile: /etc/ssl/ca.pem
```

```javascript
// Node.js connection with TLS
const client = new MongoClient('mongodb://user:pass@host:27017/ecommerce', {
  tls: true,
  tlsCAFile: '/path/to/ca.pem',
  tlsCertificateKeyFile: '/path/to/client.pem'
});
```

---

## 3. Configure Remote Access

```bash
# On the MongoDB server:
# 1. Set bindIp to 0.0.0.0 (with auth enabled!)
# 2. Open port 27017 in security group (restricted to app servers)
# 3. Ensure auth is enabled

# From remote server:
mongosh "mongodb://appuser:password@<ec2-public-ip>:27017/ecommerce?authSource=ecommerce"

# Better: Use private IP within the same VPC
mongosh "mongodb://appuser:password@<ec2-private-ip>:27017/ecommerce?authSource=ecommerce"
```

---

## 4. Deploy Node.js Backend (PM2)

```bash
# Install PM2 globally
npm install -g pm2

# Start the application
pm2 start server.js --name "ecommerce-api" -i max  # Cluster mode (all CPUs)

# PM2 ecosystem file
```

```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'ecommerce-api',
    script: 'server.js',
    instances: 'max',         // Use all CPU cores
    exec_mode: 'cluster',     // Cluster mode for load balancing
    max_memory_restart: '500M',
    env_production: {
      NODE_ENV: 'production',
      PORT: 3000,
      MONGO_URI: 'mongodb://appuser:pass@localhost:27017/ecommerce?authSource=ecommerce'
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    merge_logs: true,
    log_date_format: 'YYYY-MM-DD HH:mm:ss'
  }]
};
```

```bash
# Start with ecosystem file
pm2 start ecosystem.config.js --env production

# Key PM2 commands
pm2 status          # List all processes
pm2 logs            # View logs
pm2 monit           # Real-time monitoring
pm2 restart all     # Restart
pm2 reload all      # Zero-downtime reload (cluster mode)
pm2 save            # Save process list
pm2 startup         # Auto-start on boot
```

---

## 5. Nginx Setup (Reverse Proxy)

```bash
sudo apt install -y nginx
sudo nano /etc/nginx/sites-available/ecommerce
```

```nginx
# /etc/nginx/sites-available/ecommerce
upstream ecommerce_api {
    server 127.0.0.1:3000;
    keepalive 64;
}

server {
    listen 80;
    server_name api.yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    # SSL certificates (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000" always;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    location /api/ {
        limit_req zone=api burst=20 nodelay;

        proxy_pass http://ecommerce_api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;

        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    # Health check (no rate limit)
    location /health {
        proxy_pass http://ecommerce_api;
    }

    # Gzip compression
    gzip on;
    gzip_types application/json text/plain application/javascript;
    gzip_min_length 1000;
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/ecommerce /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl reload nginx

# SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.yourdomain.com
```

---

## 6. MongoDB Atlas (Managed Alternative)

### Why Atlas?

```
┌──────────────────────────────────────────────────────────────────┐
│  Self-Hosted                         │  Atlas (Managed)          │
├──────────────────────────────────────┼───────────────────────────┤
│  You manage: OS, patches, backups,   │  Atlas manages everything│
│  monitoring, scaling, security       │  You manage: schema, code│
│  Cost: EC2 instance + EBS storage    │  Cost: Based on tier     │
│  Control: Full                        │  Control: Limited        │
│  Expertise: DBA needed               │  Expertise: Dev-friendly │
│  Scaling: Manual                      │  Scaling: Auto-scaling   │
│  Availability: You configure HA      │  Availability: 99.995%   │
├──────────────────────────────────────┴───────────────────────────┤
│  Recommendation:                                                │
│  - Startups/small teams: Atlas (Free Tier → M10 → M30)        │
│  - Large companies with DBA team: Self-hosted or Atlas         │
│  - Development/testing: Atlas Free Tier (M0, 512MB)             │
└──────────────────────────────────────────────────────────────────┘
```

### Atlas Setup

```bash
# 1. Create account at https://cloud.mongodb.com
# 2. Create a cluster (Free Tier M0 for dev)
# 3. Configure network access (whitelist your IP or use 0.0.0.0/0 for dev)
# 4. Create database user
# 5. Get connection string

# Connection string format:
MONGO_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/ecommerce?retryWrites=true&w=majority
```

```javascript
// Node.js connection to Atlas
const mongoose = require('mongoose');

await mongoose.connect(process.env.MONGO_URI, {
  maxPoolSize: 10,
  retryWrites: true,
  w: 'majority'
});
// Atlas handles: replication, backups, monitoring, scaling, security patches
```

---

## 7. Replica Sets & Sharding

### Replica Set Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        Replica Set (rs0)                         │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│  │ PRIMARY  │───►│SECONDARY │    │SECONDARY │                  │
│  │          │───►│          │    │          │                  │
│  │ Reads +  │    │ Reads    │    │ Reads    │                  │
│  │ Writes   │    │ (async   │    │ (async   │                  │
│  │          │    │  repl)   │    │  repl)   │                  │
│  └──────────┘    └──────────┘    └──────────┘                  │
│       │                │               │                        │
│       │    Automatic Failover          │                        │
│       │    (election if primary dies)  │                        │
│                                                                  │
│  Minimum: 3 nodes (or 2 + 1 arbiter)                           │
│  Primary handles writes.                                         │
│  Secondaries replicate async.                                   │
│  If primary fails → election → new primary (10-30 seconds).    │
│                                                                  │
│  SQL equivalent:                                                 │
│  PostgreSQL streaming replication + Patroni for failover        │
│  MySQL Group Replication / InnoDB Cluster                       │
└──────────────────────────────────────────────────────────────────┘
```

### Setting Up a Replica Set

```bash
# Node 1 (primary):
mongod --replSet rs0 --port 27017 --dbpath /data/db1 --bind_ip 0.0.0.0

# Node 2 (secondary):
mongod --replSet rs0 --port 27018 --dbpath /data/db2 --bind_ip 0.0.0.0

# Node 3 (secondary):
mongod --replSet rs0 --port 27019 --dbpath /data/db3 --bind_ip 0.0.0.0

# Initialize (connect to node 1):
mongosh --port 27017
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "node1:27017", priority: 2 },
    { _id: 1, host: "node2:27018", priority: 1 },
    { _id: 2, host: "node3:27019", priority: 1 }
  ]
})

# Check status
rs.status()
```

### Sharding Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     Sharded Cluster                              │
│                                                                  │
│  ┌─────────────────────────────────────┐                        │
│  │           mongos (Router)           │  ← App connects here   │
│  │  Routes queries to correct shard    │                        │
│  └──────────────┬──────────────────────┘                        │
│                 │                                                │
│     ┌───────────┼───────────┐                                   │
│     │           │           │                                    │
│  ┌──▼──┐    ┌──▼──┐    ┌──▼──┐                                │
│  │Shard│    │Shard│    │Shard│    Each shard = replica set     │
│  │  1  │    │  2  │    │  3  │                                 │
│  │A-H  │    │I-P  │    │Q-Z  │    Data distributed by         │
│  └─────┘    └─────┘    └─────┘    shard key ranges             │
│                                                                  │
│  Config Servers (3-node replica set)                             │
│  Stores: chunk distribution metadata                             │
│                                                                  │
│  SQL equivalent:                                                 │
│  PostgreSQL + Citus (partitioning + distribution)               │
│  MySQL Vitess (Google's sharding solution)                       │
│  MongoDB's sharding is the easiest to set up of the three.     │
└──────────────────────────────────────────────────────────────────┘
```

### Shard Key Selection

```javascript
// The shard key determines how data is distributed across shards
// THIS IS THE MOST IMPORTANT DECISION in sharding

// ✅ Good shard key:
sh.shardCollection("ecommerce.orders", { customerId: "hashed" })
// Hashed: Even distribution, but range queries on customerId need all shards

sh.shardCollection("ecommerce.orders", { customerId: 1, createdAt: 1 })
// Compound: Customer's orders on same shard, range queries on createdAt work

// ❌ Bad shard key:
sh.shardCollection("ecommerce.orders", { status: 1 })
// Low cardinality: Only 5 values → all data on 5 chunks → unbalanced

sh.shardCollection("ecommerce.orders", { createdAt: 1 })
// Monotonically increasing: All writes go to the last shard (hot shard)

// Shard key selection rules:
// 1. High cardinality (many unique values)
// 2. Low frequency (values are evenly distributed)
// 3. Non-monotonic (avoid timestamps as sole key)
// 4. Supports your most common query pattern
// 5. CANNOT be changed after sharding (choose carefully!)
```

---

## 8. Backups & Monitoring

### Backup Strategies

```bash
# ──── mongodump (logical backup — like pg_dump) ────
mongodump --uri="mongodb://user:pass@host:27017/ecommerce" --out=/backups/$(date +%Y%m%d)

# Restore
mongorestore --uri="mongodb://user:pass@host:27017/ecommerce" /backups/20240115/

# ──── Compressed backup ────
mongodump --uri="..." --gzip --archive=/backups/ecommerce_$(date +%Y%m%d).gz

# ──── Specific collection ────
mongodump --uri="..." --collection=orders --out=/backups/orders/

# ──── Automated backup script ────
# /etc/cron.d/mongodb-backup
0 2 * * * root mongodump --uri="..." --gzip --archive=/backups/mongo_$(date +\%Y\%m\%d).gz && find /backups -mtime +30 -delete
```

### Atlas Backup (Managed)

```
Atlas provides:
- Continuous backups with point-in-time recovery
- Snapshots every 6 hours (configurable)
- Restore to any point in time (last 7 days)
- Cross-region backup for disaster recovery
- No management overhead
```

### Monitoring

```javascript
// ──── Basic monitoring commands ────

// Server status
db.serverStatus()

// Connection count
db.serverStatus().connections
// { current: 45, available: 955, totalCreated: 12500 }

// Operation counters
db.serverStatus().opcounters
// { insert: 10000, query: 50000, update: 8000, delete: 500 }

// WiredTiger cache stats
db.serverStatus().wiredTiger.cache
// "bytes currently in the cache": 1073741824
// "maximum bytes configured": 1610612736

// Replication lag
rs.printSecondaryReplicationInfo()

// Current operations (find slow queries)
db.currentOp({ "secs_running": { $gt: 5 } })
```

### Monitoring Tools

```
┌──────────────────────────────────────────────────────────────────┐
│  Tool                    │ Type          │ Cost                  │
├──────────────────────────┼───────────────┼───────────────────────┤
│  MongoDB Atlas Monitoring│ Managed       │ Included with Atlas   │
│  MongoDB Compass         │ GUI           │ Free                  │
│  Percona PMM             │ Self-hosted   │ Free (open source)    │
│  Datadog                 │ SaaS          │ $$                    │
│  Grafana + Prometheus    │ Self-hosted   │ Free (setup required) │
│  mongostat / mongotop    │ CLI           │ Free (included)       │
├──────────────────────────┴───────────────┴───────────────────────┤
│                                                                  │
│  Key metrics to monitor:                                         │
│  1. Query performance (slow queries, COLLSCAN)                  │
│  2. Replication lag                                              │
│  3. Connection count vs pool size                                │
│  4. WiredTiger cache utilization                                 │
│  5. Disk I/O and storage usage                                   │
│  6. Oplog window (time until oldest entry is overwritten)       │
│                                                                  │
│  Alert on:                                                       │
│  - Replication lag > 10 seconds                                 │
│  - Cache utilization > 80%                                       │
│  - Connections > 80% of max                                     │
│  - Disk usage > 80%                                              │
│  - Any COLLSCAN on production collections                       │
└──────────────────────────────────────────────────────────────────┘
```

### CLI Monitoring Tools

```bash
# mongostat — real-time server stats (like vmstat)
mongostat --uri="mongodb://user:pass@host:27017" --rowcount 10

# mongotop — time spent reading/writing per collection (like iotop)
mongotop --uri="mongodb://user:pass@host:27017" 5

# Example output:
#                     ns    total    read    write
# ecommerce.products       12ms     10ms     2ms
# ecommerce.orders         8ms      3ms      5ms
# ecommerce.sessions       2ms      1ms      1ms
```

---

## Production Deployment Checklist

```
┌──────────────────────────────────────────────────────────────────┐
│                   Production Readiness Checklist                │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Security:                                                       │
│  ☐ Authentication enabled                                       │
│  ☐ Dedicated users with least privilege                         │
│  ☐ TLS/SSL enabled                                              │
│  ☐ Network restricted (firewall / security groups)              │
│  ☐ No public internet access to MongoDB port                    │
│                                                                  │
│  High Availability:                                              │
│  ☐ Replica set with 3+ members                                 │
│  ☐ Members spread across availability zones                     │
│  ☐ Connection string includes all replica set members           │
│  ☐ Write concern: "majority" for critical data                  │
│                                                                  │
│  Performance:                                                    │
│  ☐ Indexes for all frequent queries                              │
│  ☐ WiredTiger cache sized properly (~60% of RAM)                │
│  ☐ Connection pool sized correctly                               │
│  ☐ Profiler enabled for slow queries (>100ms)                   │
│  ☐ No COLLSCAN on production queries                            │
│                                                                  │
│  Backups:                                                        │
│  ☐ Automated daily backups                                      │
│  ☐ Backup retention policy (30+ days)                           │
│  ☐ Tested backup restoration procedure                          │
│  ☐ Backups stored in different region                           │
│                                                                  │
│  Monitoring:                                                     │
│  ☐ Health check endpoint                                        │
│  ☐ Alerts on: replication lag, disk, connections, slow queries  │
│  ☐ Log aggregation                                               │
│  ☐ Dashboards for key metrics                                   │
│                                                                  │
│  Application:                                                    │
│  ☐ Graceful shutdown (close connections)                        │
│  ☐ Retry logic for transient errors                             │
│  ☐ Error handling for all MongoDB error types                    │
│  ☐ PM2 or equivalent process manager                            │
│  ☐ Nginx reverse proxy with SSL                                │
│  ☐ Rate limiting                                                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Practice Exercises

### Exercise 1: Set Up Replica Set Locally

Set up a 3-node replica set on your local machine using different ports (27017, 27018, 27019). Test automatic failover by shutting down the primary.

### Exercise 2: Deploy to Atlas

1. Create a free Atlas cluster (M0)
2. Configure network access and database user
3. Connect your Node.js app to Atlas
4. Set up Atlas alerts for slow queries and high connection count

### Exercise 3: Production Hardening

Take your development setup and add:
1. Authentication with dedicated users
2. TLS/SSL encryption
3. Automated daily backups with retention
4. Monitoring with alerts
5. PM2 + Nginx deployment

---

## Interview Q&A

**Q1: What is a MongoDB replica set and why do you need it?**
> A replica set is a group of 3+ mongod instances that maintain the same data. One is primary (handles writes), others are secondaries (replicate data). If the primary fails, an automatic election promotes a secondary — typical failover is 10-30 seconds. You need it for: high availability, data redundancy, read scaling (secondary reads), and transactions (requires replica set).

**Q2: How does MongoDB sharding differ from SQL partitioning?**
> SQL partitioning splits a table within one server (vertical scaling). MongoDB sharding distributes data across multiple servers (horizontal scaling). Sharding is transparent to the application — the `mongos` router handles query routing. Each shard is a replica set for high availability. The shard key determines distribution.

**Q3: What makes a good shard key?**
> High cardinality (many unique values), even distribution (no hot spots), supports common query patterns, and is not monotonically increasing. A hashed `_id` gives even distribution but loses range query locality. A compound key (`{ tenantId: 1, createdAt: 1 }`) balances distribution with query locality.

**Q4: How do you handle backups in MongoDB?**
> Options: (1) `mongodump/mongorestore` for logical backups. (2) Filesystem snapshots (with journaling enabled). (3) Atlas continuous backups with PITR. (4) Oplog-based incremental backups. For production: daily full backups + continuous oplog backup for point-in-time recovery. Test restoration regularly.

**Q5: MongoDB Atlas vs self-hosted — when to choose which?**
> Atlas for: teams without dedicated DBAs, startups wanting fast deployment, applications needing global distribution, and when operational overhead needs to be minimized. Self-hosted for: strict data residency requirements, cost optimization at scale, full control over configuration, and compliance requirements that prevent cloud-managed databases.
