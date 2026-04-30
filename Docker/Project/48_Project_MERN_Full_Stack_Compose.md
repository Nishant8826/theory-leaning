# 📌 Topic: Project: MERN Full Stack Compose

🟢 **Simple Explanation (Beginner)**
-----------------------------------
This is the **Master Blueprint**. 
Instead of starting the Frontend, then the Backend, then the Database separately, we use one single file to describe how they all fit together. It's the "Play" button for our entire application.

🟡 **Practical Usage**
-----------------------------------
### The Complete `docker-compose.yml`
```yaml
version: '3.8'

services:
  # 1. DATABASE
  mongodb:
    image: mongo:6.0
    restart: always
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=secret
    volumes:
      - mongo-data:/data/db

  # 2. BACKEND API
  backend:
    build: ./backend
    restart: always
    environment:
      - MONGO_URI=mongodb://admin:secret@mongodb:27017/myapp?authSource=admin
      - PORT=5000
    depends_on:
      mongodb:
        condition: service_healthy # Wait for DB to be READY

  # 3. FRONTEND (React + Nginx)
  frontend:
    build: ./frontend
    restart: always
    ports:
      - "80:80"
    depends_on:
      - backend

networks:
  default:
    name: mern-stack

volumes:
  mongo-data:
```

### The Command
```powershell
# Build and Start everything
docker compose up --build -d
```

🔵 **Intermediate Understanding**
-----------------------------------
### Service Discovery in MERN
- The Backend uses `mongodb:27017` as the connection string.
- The Frontend uses `backend:5000` (if calling from a server-side component) or the **Host IP** (if calling from the browser).

### The Build Context
Notice `build: ./backend`. Docker Compose looks into that sub-folder, finds the `Dockerfile`, and builds it automatically. You don't need to manually run `docker build`.

🔴 **Internals (Advanced)**
-----------------------------------
### Networking Segregation
A Staff Engineer would split the networks:
- **frontend-net**: Shared by Frontend and Backend.
- **backend-net**: Shared by Backend and Database.
This way, the Frontend container **physically cannot** talk to the Database container, even if it's hacked.

### Healthcheck Configuration
We should add a real healthcheck to the Database so the Backend doesn't crash on startup.
```yaml
mongodb:
  healthcheck:
    test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
    interval: 5s
    timeout: 5s
    retries: 5
```

⚫ **Staff-Level Insights**
-----------------------------------
### Multi-Environment Strategy
Use **Overlay Files**.
- `docker-compose.yml`: Base logic.
- `docker-compose.dev.yml`: Adds volume mounts for hot-reload.
- `docker-compose.prod.yml`: Adds resource limits and removed exposed ports.

### Image Naming
Don't let Compose pick random names. Use `image:` to give your built images professional tags.
```yaml
backend:
  build: ./backend
  image: mycompany/mern-backend:v1.0.0
```

🏗️ **Mental Model**
Docker Compose is the **Glue** that holds the microservices together.

⚡ **Actual Behavior**
Compose creates a single virtual bridge network and assigns every service a static DNS name matching its service name.

🧠 **Resource Behavior**
- **Startup**: Running `up --build` consumes significant CPU/Disk I/O during the compilation phase. Once running, resource usage drops to the baseline of your app.

💥 **Production Failures**
- **The "Zombie" Volume**: You changed the DB password in the YAML, but the DB keeps using the old one. 
  - **Reason**: MongoDB only sets the password the **first time** the volume is created. You must delete the volume to change the root password this way (or change it manually inside Mongo).
- **Orphaned Containers**: You renamed `backend` to `api`. The old `backend` container is still running and using port 5000!
  - **Fix**: `docker compose up --remove-orphans`.

🏢 **Best Practices**
- Always use `depends_on`.
- Use a `.env` file for all passwords.
- Name your volumes and networks explicitly.

🧪 **Debugging**
```bash
# See logs from everything in real-time
docker compose logs -f

# Restart just the backend without stopping Mongo
docker compose restart backend
```

💼 **Interview Q&A**
- **Q**: What does `depends_on` do in Docker Compose?
- **A**: It defines the order in which containers are started and stopped.
- **Q**: How do you update a single service in a Compose stack?
- **A**: `docker compose up -d --build <service_name>`.

---
Prev: [47_Project_MERN_Database_and_Persistence.md](47_Project_MERN_Database_and_Persistence.md) | Index: [00_Index.md](../00_Index.md) | Next: [49_Project_MERN_Production_Hardening.md](49_Project_MERN_Production_Hardening.md)
---
