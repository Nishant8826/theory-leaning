# 📌 Topic: Project: MERN Database and Persistence

🟢 **Simple Explanation (Beginner)**
-----------------------------------
MongoDB is the **Brain's Memory**. 
- If the container is the "body," we need to make sure that even if the body dies and a new one is born, the **Memory remains**.
- We use **Volumes** to store the database files on the "Permanent Hard Drive" (The Host) instead of inside the temporary container.

🟡 **Practical Usage**
-----------------------------------
### The Production Mongo Setup
In your `docker-compose.yml`:
```yaml
services:
  mongodb:
    image: mongo:6.0
    container_name: mern-db
    restart: always
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password123
    volumes:
      - mongo-data:/data/db # PERSISTENCE
    networks:
      - mern-network

volumes:
  mongo-data: # This volume stays even if containers are deleted
```

### Initializing the DB
You can place a `.js` or `.sh` script in `/docker-entrypoint-initdb.d/` inside the container to automatically create users or collections the first time it starts.

🔵 **Intermediate Understanding**
-----------------------------------
### Database Security
1. **Authentication**: Never run Mongo without a username and password in production.
2. **Network Isolation**: Notice the `mongodb` service is **NOT** mapping any ports to the host (`ports: - "27017:27017"` is missing).
   - Only the `backend` container can talk to it.
   - A hacker on the internet cannot even "see" your database port.

### WiredTiger Engine
Modern MongoDB uses the WiredTiger storage engine. It creates a lot of files. 
**Staff Tip**: Don't use a "Bind Mount" for Mongo on Windows/Mac as the performance is 10x slower. Use **Named Volumes**.

🔴 **Internals (Advanced)**
-----------------------------------
### Journaling
MongoDB writes to a "Journal" first before the actual data files. If the container crashes, Mongo reads the journal to recover.
**Advanced Setup**: Map the journal to a separate volume or a high-speed SSD for maximum reliability.

### The Lock File
Mongo creates a `mongod.lock` file. If the container is killed forcefully, this file might prevent it from starting again. Docker's `--restart always` policy usually handles this, but sometimes you have to manually delete the lock from the volume.

⚫ **Staff-Level Insights**
-----------------------------------
### Backup Strategy (Mongodump)
A volume is not a backup! If the host's hard drive dies, the volume is gone.
**Staff Automation**:
```bash
# Run a temporary container to dump the data
docker exec mern-db sh -c 'exec mongodump -d myapp --archive' > /backups/db_$(date +%F).archive
```

### Sidecar Backup
Run a separate container that wakes up every 24 hours, runs the command above, and pushes the file to AWS S3. This is **Disaster Recovery**.

🏗️ **Mental Model**
MongoDB is a **External State Store**. The container is just a "Plug" that connects the state to the network.

⚡ **Actual Behavior**
All data is stored in `/var/lib/docker/volumes/mongo-data/_data` on the Linux host.

🧠 **Resource Behavior**
- **Memory**: MongoDB will try to use 50% of the available RAM for its cache. 
- **Staff Fix**: Limit it!
  `command: ["--wiredTigerCacheSizeGB", "0.25"]`

💥 **Production Failures**
- **Data Loss**: You used `docker compose down -v`. The `-v` flag deletes all volumes! 
  - **Staff Rule**: Never use `-v` in production.
- **Permission Denied**: You tried to map a folder on your Windows Desktop to `/data/db`. Mongo can't set the correct permissions on Windows folders.

🏢 **Best Practices**
- Use **Named Volumes**.
- **Enable Auth** (Username/Password).
- **No public ports**.
- Limit **RAM usage**.

🧪 **Debugging**
```bash
# Check if Mongo is alive and healthy
docker exec mern-db mongosh --eval "db.adminCommand('ping')"

# Look at the data files on the host
docker volume inspect mongo-data
```

💼 **Interview Q&A**
- **Q**: Why shouldn't we expose the MongoDB port (27017) to the host in production?
- **A**: For security. Only the backend API needs to talk to the database; exposing it to the public internet invite attacks.
- **Q**: What happens to your data if you delete the MongoDB container?
- **A**: If you used a volume, the data remains safe on the host. If not, the data is lost forever.

---
Prev: [46_Project_MERN_Frontend_Optimization.md](46_Project_MERN_Frontend_Optimization.md) | Index: [00_Index.md](../00_Index.md) | Next: [48_Project_MERN_Full_Stack_Compose.md](48_Project_MERN_Full_Stack_Compose.md)
---
