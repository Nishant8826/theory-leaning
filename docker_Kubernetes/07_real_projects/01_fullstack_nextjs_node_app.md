# Fullstack Nextjs Node App

## Why This Exists
In the real world, applications are rarely just one piece of software. A modern application typically needs a beautiful user interface (Frontend), a brain to process business logic (Backend), and a secure vault to store data (Database). We use Docker to easily bundle and run all these different moving parts together without them interfering with each other.

## Real World Analogy
Think of a **Restaurant**:
*   **Frontend (Next.js)** is the **Dining Area** and the **Menu**. It's what the customer sees and interacts with.
*   **Backend (Node.js)** is the **Kitchen**. The waiters take your order (API request) to the kitchen, where the chefs process it.
*   **Database (PostgreSQL/MongoDB)** is the **Pantry**. The chefs grab ingredients from here to prepare your meal.
Docker Compose is like the **Restaurant Manager**, ensuring the dining area, kitchen, and pantry are all open, connected, and working together smoothly.

## Core Concepts
*   **Multi-Container Applications:** Running several containers that work together as a single application.
*   **Docker Compose:** A tool that lets you define and run multi-container Docker applications using a single YAML file.
*   **Internal Networking:** Docker automatically creates a private network so your frontend container can talk to your backend container simply by using its name (e.g., `http://backend:5000`).

## Architecture / Flow
1. User opens the browser and hits the **Next.js Frontend**.
2. The user clicks "Show My Profile". The Next.js app sends an HTTP GET request to the **Node.js Backend**.
3. The Node.js Backend receives the request and asks the **Database** for the user's data.
4. The Database returns the data to Node.js, which sends it back to Next.js, which finally displays it to the user.

## Practical Commands
*   `docker-compose up` - Starts all the containers defined in your `docker-compose.yml`.
*   `docker-compose up -d` - Starts them in the background (detached mode).
*   `docker-compose down` - Stops and removes all the containers and networks.
*   `docker-compose logs -f` - Follows the logs of all your running services.

## Hands-On Exercise
Create a `docker-compose.yml` file that defines three services: `frontend`, `backend`, and `db`. Start them all with a single `docker-compose up` command and verify you can access the frontend on your local browser.

## Mini Project
**"Task Master"**
Build a simple Todo application. 
*   **Next.js:** A page with an input field to add tasks and a list showing current tasks.
*   **Node.js/Express:** API endpoints like `POST /tasks` and `GET /tasks`.
*   **MongoDB:** Stores the actual tasks. Wrap them all in Docker Compose.

## Real Production Usage
Startups often deploy their entire stack (Frontend, Backend, DB) on a single powerful server using Docker Compose because it is simple and cheap. As they grow, they might move to Kubernetes, allowing them to scale the Backend (run 10 kitchens) while keeping the Frontend smaller (run 2 dining areas).

## Common Mistakes
*   **Hardcoding `localhost`:** Inside a Docker network, `localhost` means "inside this specific container". Your frontend container cannot reach the backend by calling `localhost:5000`. It must call `backend:5000` (the service name).
*   **Forgetting Volumes:** If you don't attach a Docker Volume to your database container, all your user data will be permanently deleted the moment the container restarts!

## Debugging Guide
*   **Database won't connect?** Make sure the backend waits for the database to be fully ready. Sometimes the backend boots up faster than the database.
*   **Frontend looks broken?** Check the browser console. If API calls fail, check the network tab to see if it's pointing to the correct backend URL. Use `docker logs <backend-container-id>` to see if the backend threw an error.

## Best Practices
*   **Environment Variables:** Never hardcode database passwords in your code. Pass them in using `.env` files and Docker Compose environment variables.
*   **Separate Dockerfiles:** Keep one `Dockerfile` in your frontend folder and one in your backend folder. They should be built independently.
*   **Use `.dockerignore`:** Prevent copying `node_modules` from your local machine into the container. Let the container run `npm install` itself.

## Interview Questions
*   **Q: How do two containers communicate in Docker Compose?**
    *   *A: Docker Compose automatically creates a custom bridge network. Containers can talk to each other using their service names defined in the `docker-compose.yml` as hostnames.*
*   **Q: How do you ensure database data survives container restarts?**
    *   *A: By using Docker Volumes to map a directory on the host machine to the database storage directory inside the container.*

## Summary
Building fullstack apps with Docker teaches you how different pieces of software communicate over a network. It moves you from writing isolated scripts to orchestrating real, multi-tier software systems just like they do in the industry.

---
Prev: [Index](../00_index.md) | Index: [Index](../00_index.md) | Next: [02_microservices_ecommerce.md](./02_microservices_ecommerce.md)
