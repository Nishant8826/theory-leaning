# Introduction to Docker Compose

---

### What
**Docker Compose** is a tool that allows you to define and run multi-container Docker applications. Instead of running 5 massive `docker run` commands manually in your terminal every time you want to start a project, you write all those settings down in one file: `docker-compose.yml`.

---

### Why
A real application is never just one container. A standard app usually requires:
- Next.js Frontend (Container 1)
- Node.js API (Container 2)
- Postgres Database (Container 3)
- Redis Cache (Container 4)

Typing out the `docker run` commands with `-v` (volumes), `-e` (env vars), and `-p` (ports) for all four containers every single day is exhausting. Compose turns this into a single command: `docker-compose up`.

---

### How
Docker Compose uses **YAML** (a very simple data configuration language). 
1. You create a `docker-compose.yml` file.
2. Inside, you define a `services` block. Each service is one container.
3. For each service, you specify which Image it uses, what Ports to open, and what passwords (Env Vars) it needs.
4. Compose automatically creates a private internal **Network** bridging all these containers so they can securely talk to each other using their service names instead of IP addresses!

---

### Implementation

Here is a basic Compose file for a React app and a Node.js app running together.

```yaml
# File: docker-compose.yml
version: '3.8'

services:
  # Container 1: The Backend API
  api:
    build: ./backend              # Points to the folder with the Backend Dockerfile
    ports:
      - "5000:5000"               # Map host 5000 to container 5000
    environment:
      - DB_PASS=secret123         # Set Env Variables

  # Container 2: The Frontend
  frontend:
    build: ./frontend             # Points to the folder with Frontend Dockerfile
    ports:
      - "3000:3000"
    depends_on:
      - api                       # Tells compose not to start React until API is ready
```

---

### Steps
1. Create `docker-compose.yml` in the absolute root of your project workspace.
2. Define your services.
3. In your terminal, run `docker-compose up -d` to launch the entire stack in the background.
4. To shut down the entire stack (and clean the network), run `docker-compose down`.

---

### Integration

* **React/Next.js and Node.js networking:** When using Docker Compose, Compose automatically creates a DNS system. If your React Frontend container needs to fetch data from the API container, it does **not** fetch `http://localhost:5000`. It simply fetches `http://api:5000`. Compose acts like a router, instantly resolving the word "api" to the correct container!
* **Full-Stack Projects:** Compose is the de-facto standard for local development. New developers simply clone the git repository and type `docker-compose up`. Within 60 seconds, the frontend, backend, and DB launch simultaneously perfectly configured. 

---

### Impact
Docker Compose eliminates horrific "startup scripts", replaces them with clean declarative syntax, handles isolated networking automatically, and coordinates the startup sequences of complex enterprise architectures effortlessly.

---

### Interview Questions
1. **What is Docker Compose and why is it used?**
   *Answer: It is an orchestration tool used to define, configure, and launch multi-container Docker applications systematically using a single YAML file instead of multiple manual CLI commands.*
2. **How do containers inside the same `docker-compose.yml` network talk to each other?**
   *Answer: Compose automatically attaches them to a shared default network and provides automatic DNS resolution. Containers ping each other using the exact "Service name" defined in the YAML file (e.g., `redis` or `db`).*
3. **What is the difference between `docker-compose stop` and `docker-compose down`?**
   *Answer: `stop` only pauses the containers, preserving their network mapping. `down` actively stops and destroys the containers, the default network, and clears all non-persisted state.*

---

### Summary
* Compose files replace long, tedious terminal commands.
* Use YAML syntax to blueprint all your architecture in one place.
* `docker-compose up -d` starts the entire system.
* Services can talk to each other by name!

---
Prev : [06_writing_dockerfiles.md](./06_writing_dockerfiles.md) | Next : [08_docker_compose_full_stack.md](./08_docker_compose_full_stack.md)
