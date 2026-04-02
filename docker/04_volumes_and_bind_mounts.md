# Volumes, Bind Mounts, and Environment Variables

---

### What
Since containers destroy all new data when they restart or are deleted, we need a way to permanently save files (like User Uploads or Database logic).
- **Volumes:** A safely managed folder located deep inside Docker's hidden architecture on your computer. Containers can securely read/write to it.
- **Bind Mounts:** Connecting a specific, visible folder on your host machine (e.g., `C:/Users/Desktop/my-code`) directly to a folder inside the live container.
- **Environment Variables:** Secure key-value pairs (like API keys) injected into the container exactly at runtime without hardcoding them into the image.

---

### Why
- **Volumes:** This is how we allow a MongoDB container to save user accounts. If the MongoDB container crashes, we launch a new one and attach the old Volume. No data lost!
- **Bind Mounts:** This provides **Hot Reloading** for developers! If you change a file on your Windows Desktop, it instantly updates inside the isolated Docker container without needing to rebuild the image.
- **Env Variables:** If you put your Stripe API key into a Docker Image and share the Image on Docker Hub, the whole world can steal your money. Variables must be injected dynamically!

---

### How
You assign volumes, mounts, and env variables directly via the command line when starting the container.

---

### Implementation

Let's look at a Node.js project being run via Terminal flags.

```bash
# --- 1. DOCKER VOLUMES (Best for Databases) ---

# Create a new, permanent hidden folder managed by Docker
docker volume create pg_data

# Run Postgres, map the invisible volume to the container's internal data path
docker run -d --name my_db \
  -v pg_data:/var/lib/postgresql/data \
  postgres


# --- 2. BIND MOUNTS (Best for Developers / Hot Reload) ---

# Run our Node.js app! 
# We map the present working directory "$(pwd)" to "/app" inside the container.
# If I edit index.js on my Windows machine, the container's /app/index.js changes instantly.
docker run -d --name my_node_app \
  -v "$(pwd)":/app \
  my_node_image


# --- 3. ENVIRONMENT VARIABLES (Best for Secrets) ---

# Inject variables at runtime using the -e flag
docker run -d --name my_backend \
  -e PORT=8080 \
  -e DATABASE_URL="mongodb://..." \
  -e STRIPE_KEY="sk_live_12345" \
  my_node_image
```

---

### Steps
1. Identify if you need developer syncing (Bind Mounts) or secure data persistence (Volumes).
2. For databases, always use Volumes. For frontend/backend coding workflows, use Bind Mounts for instant refreshing.
3. In your code, always use `process.env.VAR_NAME` instead of hardcoded strings.
4. Inject keys at runtime using the `-e` flag.

---

### Integration

* **React / Next.js Development:** Use a Bind Mount to connect your `styles` and `components` folders. This ensures Next.js Fast Refresh works perfectly even though Next.js is running inside a Docker box.
* **Node.js Backend:** Inject your `JWT_SECRET` and `OPENAI_API_KEY` exclusively via environment variables when spinning up the production container.
* **Databases:** A Postgres or MongoDB container without a Volume is useless. If the container stops or your server restarts, your entire database is obliterated. Always attach a Docker Volume.

---

### Impact
Volumes separate the lifecycle of your application (which should be stateless and destroyable at any time) from your data (which must live forever). It is the foundational concept for building scalable, cloud-native apps.

---

### Interview Questions
1. **Explain the difference between a Volume and a Bind Mount.**
   *Answer: Volumes are fully managed by Docker and stored in a protected internal directory, ideal for persistent data like databases. Bind Mounts map an exact file path on the host machine to the container, heavily used for dev workflows to enable hot reloading.*
2. **Why should we never hardcode secrets inside a Docker Image?**
   *Answer: Docker Images contain instructions in read-only layers. Anyone who pulls the image or executes a reverse-engineering command (`docker history`) can extract hardcoded passwords effortlessly.*
3. **If I delete a container, what happens to the attached Docker Volume?**
   *Answer: The Volume persists safely on the host machine. You can start a completely new container and mount the same volume to instantly restore state.*

---

### Summary
* By default, all data inside a container is temporary.
* **Volumes** permanently backup data safely inside Docker.
* **Bind Mounts** sync local folders into the container (perfect for Hot Reloading).
* **Env Variables** (`-e`) secure dynamic data away from your permanent image stack.

---
Prev : [03_core_concepts_images_containers.md](./03_core_concepts_images_containers.md) | Next : [05_working_with_docker_commands.md](./05_working_with_docker_commands.md)
