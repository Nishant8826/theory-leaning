# 📌 Topic: DB Containers (Mongo and Postgres)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Running a database in a container is easy. You just run the image and give it a volume. It's great for development because you don't have to install anything on your laptop.
**Expert**: Running databases in production containers is a **Systems Engineering challenge**. It requires tuning **Memory Overcommit**, **I/O Schedulers**, and **Kernel Parameters** (like HugePages). Unlike stateless web apps, databases are "Sensitive Neighbors." They expect exclusive access to hardware. Staff-level engineering requires configuring **Graceful Shutdowns** (so the DB can flush its WAL—Write Ahead Log), managing **Secrets** for passwords securely, and implementing **Probes** that know the difference between "The container is up" and "The database is ready to accept queries."

## 🏗️ Mental Model
- **Web App Container**: A tenant in a hotel. They can move to a new room (different server) easily.
- **Database Container**: A grand piano in a house. It is heavy, it needs a specific environment (Climate/Vibration control), and if you move it, you have to be very careful not to break it.

## ⚡ Actual Behavior
- **Initialization**: Official DB images have an `/docker-entrypoint-initdb.d/` folder. Any `.sql` or `.sh` script placed there is executed automatically the first time the database is created.
- **Signals**: Databases need time to shut down. If you `docker stop` a DB and it takes 15 seconds to flush to disk, but your orchestrator kills it at 10 seconds, you get **Data Corruption**.

## 🔬 Internal Mechanics (The Storage Path)
1. **The WAL (Write Ahead Log)**: Every change is first written to a log file.
2. **The Data Files**: Periodically, the log is flushed to the main data files.
3. **Docker Volume**: Bypasses the OverlayFS. The DB engine talks directly to the host's filesystem (XFS/Ext4). This is critical because databases perform many small, random writes that OverlayFS would be 10x slower at.

## 🔁 Execution Flow (Postgres Startup)
1. Container starts.
2. Entrypoint script checks if `/var/lib/postgresql/data` is empty.
3. If empty: Runs `initdb`, sets password, runs scripts in `initdb.d`.
4. If not empty: Skips initialization and starts the server process.
5. Server starts recovery mode (checking WAL for inconsistencies).
6. Server opens port 5432.

## 🧠 Resource Behavior
- **Memory**: Databases (especially Postgres) use the **OS Page Cache**. If you limit a DB container to 1GB, but the host has 64GB, the DB might try to use more than its limit for caching, leading to an OOM Kill.
- **Storage**: Databases are "IOPS Hungry." Ensure the host disk is an NVMe SSD and not a network-attached disk (EBS Standard) for production.

## 📐 ASCII Diagrams (REQUIRED)

```text
       DATABASE CONTAINER ARCHITECTURE
       
[ DB CLIENT ] --( Port 5432 )--> [ DB ENGINE ]
                                    |
          +-------------------------+-------------------------+
          | (High Speed Path)                                 | (Slow Path)
          v                                                   v
 [ DOCKER VOLUME ]                                   [ CONTAINER LAYER ]
(/var/lib/postgresql)                                  ( /etc/config )
          |                                                   |
 [ HOST FS (XFS) ]                                    [ OVERLAY2 FS ]
```

## 🔍 Code (Hardened DB Compose)
```yaml
services:
  db:
    image: postgres:15-alpine
    restart: always
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - pgdata:/var/lib/postgresql/data
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
secrets:
  db_password:
    file: ./db_password.txt
```

## 💥 Production Failures
- **The "Zombie Lock"**: A DB container crashes. The lock file (`postmaster.pid`) stays in the volume. A new container starts, sees the lock file, and thinks another instance is running. It refuses to start.
  *Fix*: Use a better entrypoint script or manually delete the lock file.
- **Corruption on Kill**: Running a DB without a proper volume. The host loses power. Because OverlayFS doesn't guarantee atomic writes as strictly as Ext4, the database files are irrecoverable.

## 🧪 Real-time Q&A
**Q: Should I run my database in Docker or use a managed service like AWS RDS?**
**A**: For production, use **RDS**. It handles backups, patching, and high availability automatically. Use Docker for **Development**, **CI/CD Testing**, and **Edge/On-premise** deployments where managed services aren't available. The "Staff" answer is: "Only manage a database yourself if you have a full-time DBA team."

## ⚠️ Edge Cases
- **Postgres Shared Memory**: Older Postgres versions required a specific `--shm-size` to be set in Docker, otherwise complex queries would fail with "Out of memory" even if RAM was free.

## 🏢 Best Practices
- **Use Alpine images**: To reduce vulnerabilities.
- **Never store passwords in Environment Variables**: Use Docker Secrets or mount a config file.
- **Strict Stop Timeout**: Set `stop_grace_period: 2m` to give the DB plenty of time to shut down.

## ⚖️ Trade-offs
| Metric | Docker DB | Managed DB (RDS) |
| :--- | :--- | :--- |
| **Control** | **Absolute** | Limited |
| **Cost** | Low (Compute only)| High (Service fee) |
| **Operational Effort**| High | **Low** |

## 💼 Interview Q&A
**Q: How do you handle a database migration (schema change) when deploying a new version of a containerized app?**
**A**: I use an **Init-Container** or a migration stage in the deployment. Before the new app container starts, I run a transient container with the same code but a command like `npm run migrate`. This container connects to the database, performs the schema updates, and exits. Only if this migration succeeds does the orchestrator (Compose/K8s) proceed to update the main application containers. This ensures that the code and the database schema are always in sync.

## 🧩 Practice Problems
1. Create a Postgres container and use a `.sql` file in `initdb.d` to create a table and insert data automatically.
2. Simulate a "Thundering Herd" by starting 100 containers that all try to connect to the same Postgres instance. Observe the "Max Connections" error and fix it in the DB config.

---
Prev: [03_Data_Persistence.md](./03_Data_Persistence.md) | Index: [00_Index.md](../00_Index.md) | Next: [05_IO_Performance.md](./05_IO_Performance.md)
---
