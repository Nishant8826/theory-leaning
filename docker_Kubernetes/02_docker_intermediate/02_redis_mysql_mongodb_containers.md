# Redis, MySQL, and MongoDB Containers

## Why This Exists
Running databases and caches manually on your local machine is painful. You have to install the software, manage background services, handle conflicting versions, and clean up when you're done.

Dockerizing stateful services like **Redis** (caching), **MySQL** (relational database), and **MongoDB** (NoSQL database) allows you to spin up fully configured databases in seconds without polluting your host machine. However, databases are *stateful*—meaning they hold data that must survive container restarts. Understanding how to handle data persistence and security for these containers is critical.

## Real World Analogy
Think of a database container like a **Temporary Storage Unit**.
- If you store your belongings (data) inside the unit and the unit is demolished (container deleted), your belongings are lost.
- To keep your belongings safe, you need to connect the unit to a **Permanent Locker** (Docker Volume) outside the unit. Even if the storage unit is replaced, the locker remains untouched.

## Core Concepts
- **Stateful vs Stateless**: Apps are usually stateless (can be destroyed and recreated freely). Databases are stateful (data must be preserved).
- **Data Persistence**: Using Volumes to ensure data survives when a database container stops or is deleted.
- **Environment Variables**: Used to set initial passwords, database names, and user credentials.

## Architecture / Flow

```text
[ Web Application ]
       │
       ▼ (Connection String)
+-------------------------+
| Database Container      |
+-------------------------+
       │
       ▼ (Mounts)
+-------------------------+
| Docker Volume           | (Stores actual data files)
+-------------------------+
```

## Practical Commands

### 1. Redis (Cache)
```bash
# Run Redis with data persistence
docker run -d --name my-redis -p 6379:6379 -v redis-data:/data redis:alpine

# Connect to Redis CLI
docker exec -it my-redis redis-cli
```

### 2. MongoDB (NoSQL)
```bash
# Run MongoDB with username and password
docker run -d --name my-mongo -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=secret -p 27017:27017 -v mongo-data:/data/db mongo:latest
```

### 3. MySQL (SQL)
```bash
# Run MySQL
docker run -d --name my-mysql -e MYSQL_ROOT_PASSWORD=secret -e MYSQL_DATABASE=myapp -p 3306:3306 -v mysql-data:/var/lib/mysql mysql:latest
```

## Hands-On Exercise
Let's run a Redis container and test data persistence.

1. Start Redis with a volume:
   ```bash
   docker run -d --name test-redis -v test-redis-data:/data redis:alpine
   ```
2. Set a value inside Redis:
   ```bash
   docker exec -it test-redis redis-cli set mykey "Hello Docker"
   ```
3. Delete the container:
   ```bash
   docker rm -f test-redis
   ```
4. Start a new container using the same volume:
   ```bash
   docker run -d --name test-redis-new -v test-redis-data:/data redis:alpine
   ```
5. Check if the value is still there:
   ```bash
   docker exec -it test-redis-new redis-cli get mykey
   # Output should be "Hello Docker"
   ```

## Mini Project
**Task**: Set up a Node.js app connected to a MongoDB database with data persistence using Docker Compose.

1. Create a `docker-compose.yml`:
   ```yaml
   version: '3.8'
   services:
     app:
       image: node:22-alpine
       command: node -e "const MongoClient = require('mongodb').MongoClient; MongoClient.connect('mongodb://db:27017').then(() => console.log('Connected to DB')).catch(err => console.error(err));"
       # Note: In real life, you'd need to install the mongodb driver first
       depends_on:
         - db

     db:
       image: mongo:latest
       ports:
         - "27017:27017"
       volumes:
         - mongo-store:/data/db
       environment:
         - MONGO_INITDB_ROOT_USERNAME=user
         - MONGO_INITDB_ROOT_PASSWORD=pass

   volumes:
     mongo-store:
   ```

## Real Production Usage
- **To Dockerize or Not?**: While Docker is excellent for development databases, many companies prefer **Managed Database Services** (like AWS RDS, MongoDB Atlas, or AWS ElastiCache) in production. These services handle backups, patching, and high availability automatically.
- **StatefulSets**: If you *do* run databases in containers in production (e.g., on Kubernetes), you use **StatefulSets** rather than standard deployments to manage stable network IDs and storage.

## Common Mistakes
- **Forgetting Volumes**: Running a database without a volume. When the container stops, your data is gone forever!
- **Using `latest` tags**: Using `mysql:latest` can break your app if a new major version is released. Always use specific tags like `mysql:8.0`.
- **Not securing exposed ports**: Exposing database ports (like `3306`) to the public internet without strong passwords.

## Debugging Guide
- **Connection Refused**: 
  - Ensure the database container is running (`docker ps`).
  - Verify you are using the correct port and hostname (service name in Compose).
- **Authentication Failed**: Verify that the environment variables for passwords match your connection string.

## Best Practices
- **Use `.env` files**: Never hardcode database passwords in your `docker-compose.yml`. Use a `.env` file and reference variables.
- **Initialize scripts**: Most official database images allow you to put `.sql` or `.js` scripts in a specific directory (e.g., `/docker-entrypoint-initdb.d/`) to run automatically on first startup.

## Interview Questions
1. **Why do we use volumes with database containers?**
   *Answer*: Containers are ephemeral. When they are deleted, their data is lost. Volumes store data on the host machine, ensuring it persists across container lifecycles.
2. **Should you run databases in Docker in production?**
   *Answer*: It is highly recommended for development to ensure consistency. However, for production, many prefer managed services for easier backups, scaling, and high availability, though running them in containers is possible with tools like Kubernetes StatefulSets.

## Summary
Dockerizing databases simplifies development environments immensely. By mastering Volumes and Environment Variables, you can safely manage Redis, MySQL, and MongoDB containers without risking data loss.

---
Prev: [01_reverse_proxy_nginx.md](./01_reverse_proxy_nginx.md) | Index: [Index](../00_index.md) | Next: [03_logging.md](./03_logging.md)
