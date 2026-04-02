# Example: Full-Stack App with Docker Compose

---

### What
We are going to bring all our knowledge together. We will build a complete full-stack `docker-compose.yml` architecture bridging a Node.js backend to an automated MongoDB Database.

---

### Why
Real databases require passwords and permanent storage. Real backends require database connection strings. Orchestrating this manually via the terminal is practically impossible without making a typo. A Compose file locks these configuration relationships into stone.

---

### How
1. We define the `db` service using the official MongoDB image from Docker Hub.
2. We map a permanent Volume to the `db` so user data isn't deleted.
3. We define the `backend` service, pointing it to our custom Node.js code.
4. We set the connection string inside the `backend` to point dynamically to `mongodb://db:27017` using Docker's internal DNS.

---

### Implementation

Create this `docker-compose.yml` at the root of your Node.js API project.

```yaml
version: '3.8'

services:
  # 1. THE DATABASE
  db:
    image: mongo:latest              # Don't build our own, use the official one!
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db          # Map invisible volume to ensure data permanence
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: supersecretpassword123

  # 2. THE CUSTOM NODE BACKEND
  backend:
    build: .                         # Look in this current folder for a Dockerfile
    ports:
      - "5000:5000"
    depends_on:
      - db                           # Don't boot Node until Mongo is booting
    environment:
      # Observe the magic DNS! We connect to "db" (the service name above), 
      # not localhost! We also pass in the matching passwords securely.
      - DATABASE_URI=mongodb://admin:supersecretpassword123@db:27017/?authSource=admin
      - PORT=5000

# 3. REGISTER THE PERMANENT VOLUME
volumes:
  mongo_data:                        # Must declare the Volume root explicitly here
```

---

### Steps
1. In your Node.js code (`server.js`), connect your Mongoose/MongoDB driver directly to `process.env.DATABASE_URI`.
2. Confirm the `Dockerfile` exists for your Node project.
3. Run `docker-compose up -d`.
4. Run `docker ps`. You will see two containers running! One custom Node app, one massive MongoDB database instance.

---

### Integration

* **React/Next.js/Node.js:** If your frontend is Next.js, and you require SSR (Server Side Rendering) data from the API, Server components in Next.js will fetch `http://backend:5000`. Remember, if the user interacts via their **Browser** (Client-side), the browser must connect to `localhost:5000`, because the browser is physically on your physical machine, outside the private Docker internal network!

---

### Impact
You just spun up a fully authenticated, persistent NoSQL database alongside a custom Node backend in one command. You didn't have to download the MongoDB MSI installer, manage Windows Services, or configure paths. It is flawlessly clean.

---

### Interview Questions
1. **In the Compose file, why must you formally declare `volumes` at the very bottom?**
   *Answer: While bind-mounts hook directly into the Host file-system cleanly, internal Docker Volumes must be actively registered with Docker's core daemon so it knows to allocate hidden filesystem space to persist them beyond the Compose lifecycle.*
2. **If a React browser client is trying to fetch from the Node backend, what URL does it use?**
   *Answer: It must fetch `localhost:[port]`. The internal Compose DNS (e.g., `http://backend`) is absolutely invisible to the user's browser; it only exists inside the network connecting the containers securely.*

---

### Summary
* Compose effortlessly links public software (MongoDB) with your custom software (Node.js).
* Environment variables form the "connection strings" between the services.
* Compose auto-generates internal DNS logic (`db:27017`).
* Always define Volume keys at the end of the file for databases!

---
Prev : [07_docker_compose_basics.md](./07_docker_compose_basics.md) | Next : [09_dockerizing_nodejs_backend.md](./09_dockerizing_nodejs_backend.md)
