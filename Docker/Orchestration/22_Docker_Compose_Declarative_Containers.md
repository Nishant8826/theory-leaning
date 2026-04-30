# 📌 Topic: Docker Compose: Declarative Containers

🟢 **Simple Explanation (Beginner)**
-----------------------------------
Imagine you are building a **Model Airplane**.
- **`docker run`** is like gluing one piece at a time manually. If you mess up, you have to remember exactly what you did.
- **Docker Compose** is like a **Blueprint**. You write down all the pieces, where they go, and how they connect. Then you just press a button, and the whole airplane is built automatically.

Instead of typing 10 long commands to start your App, DB, Cache, and Proxy, you write one `docker-compose.yml` file and run `docker-compose up`.

🟡 **Practical Usage**
-----------------------------------
### The `docker-compose.yml` file
This is a **YAML** file. Spaces matter!

```yaml
version: '3.8' # Use the latest version

services:
  web:
    build: .
    ports:
      - "8080:80"
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password123
```

### Essential Commands
- `docker-compose up -d`: Build and start everything in the background.
- `docker-compose ps`: See the status of your app "stack."
- `docker-compose logs -f`: See logs from all services at once (color-coded!).
- `docker-compose down`: Stop and **delete** all containers and networks. (Data in volumes is safe).

🔵 **Intermediate Understanding**
-----------------------------------
### Declarative vs. Imperative
- **Imperative (`docker run`)**: You tell Docker **WHAT TO DO** ("Run this, map that").
- **Declarative (Compose)**: You tell Docker **HOW IT SHOULD LOOK** ("I want a web app and a DB connected on this network"). If the state is wrong, Compose fixes it.

### Automatic Networking
When you run `docker-compose up`, it automatically creates a **private network** for your project.
- Your `web` service can talk to `db` using the hostname `db`.
- You don't have to create the network manually.

🔴 **Internals (Advanced)**
-----------------------------------
### The Project Name
Compose uses your **folder name** as the project name by default. 
If your folder is `my-store`, containers will be named `my-store-web-1` and `my-store-db-1`.
This allows you to run the same project multiple times on one server by just changing the folder name.

### State Tracking
Compose doesn't have its own database. It "finds" its containers by looking at **Docker Labels**. When it creates a container, it adds a label `com.docker.compose.project=my-project`. When you run `down`, it looks for all containers with that label and deletes them.

⚫ **Staff-Level Insights**
-----------------------------------
### Docker Compose V2
Historically, `docker-compose` was a separate Python script.
**Staff Note**: In 2023, Docker moved it into the core CLI as a Go plugin. You should now use **`docker compose`** (no hyphen) instead of `docker-compose`. It is much faster and more stable.

### The `depends_on` Fallacy
`depends_on` only waits for the container to **start**, not for the app inside to be **ready**.
**Staff Solution**: If your Node.js app starts before Postgres is ready to accept connections, it will crash. Use a **Healthcheck** or a "wait-for-it" script.
```yaml
services:
  web:
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
```

🏗️ **Mental Model**
Docker Compose is a **Project Orchestrator**.

⚡ **Actual Behavior**
Compose parses your YAML, converts it into a series of Docker API calls, and executes them in order.

🧠 **Resource Behavior**
- **Orphaned Containers**: If you remove a service from your YAML and run `up`, the old container keeps running! Use `docker compose up --remove-orphans`.

💥 **Production Failures**
- **YAML Indentation Error**: One extra space in your `.yml` file and the whole thing fails with a cryptic error message.
- **Port Conflict in Project A vs B**: You have two projects, both trying to map to host port 8080. Compose will fail to start the second one.

🏢 **Best Practices**
- Always use a `.env` file for secrets, don't hardcode them in the YAML.
- Use `version: '3.8'` or higher.
- Keep your production and development YAML files separate (e.g., `docker-compose.yml` and `docker-compose.prod.yml`).

🧪 **Debugging**
```bash
# Validate your YAML file without running it
docker compose config

# Restart just one service
docker compose restart web
```

💼 **Interview Q&A**
- **Q**: What is Docker Compose used for?
- **A**: For defining and running multi-container Docker applications using a single YAML file.
- **Q**: How do you pass environment variables to Compose?
- **A**: Through a `.env` file in the same directory or via the `environment:` key in the YAML.

---
Prev: [../Storage/21_Tmpfs_Mounts_and_Data_Security.md](../Storage/21_Tmpfs_Mounts_and_Data_Security.md) | Index: [00_Index.md](../00_Index.md) | Next: [23_Managing_Multi_Container_Applications.md](23_Managing_Multi_Container_Applications.md)
---
