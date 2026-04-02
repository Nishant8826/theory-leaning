# Docker Architecture

---

### What
Docker isn't just one magic button. It is a **Client-Server architecture** made of several moving pieces working together.
- **Docker Client:** The CLI (Command Line Interface). It's what you type into terminal (e.g., `docker run`).
- **Docker Daemon (Server):** The invisible background program (Engine) that does the actual heavy lifting of building and running containers.
- **Docker Registry:** The cloud library (like Docker Hub) where people share images.
- **Docker Image:** The read-only blueprint for a container.
- **Docker Container:** A running, active instance of the Image.

---

### Why
Understanding this architecture prevents catastrophic mistakes. For example, knowing that "Images are read-only blueprints" ensures you don't accidentally try to save permanent user data *inside* a container's filesystem (which gets wiped when the container stops).

---

### How
1. You type `docker pull node:18` into the **Client**.
2. The Client tells the **Daemon** to get it.
3. The Daemon talks to the **Registry** (Docker Hub) and downloads the blueprint (Image).
4. The Daemon saves the Image to your hard drive.
5. You type `docker run node:18`. The Daemon spins up an active **Container** from that blueprint.

---

### Implementation

Let's visualize the architecture through basic CLI interactions.

```bash
# 1. THE CLIENT sends a request to the DAEMON
docker pull ubuntu

# 2. THE REGISTRY: The Daemon downloads 'ubuntu' from Docker Hub

# 3. THE IMAGE: To view your local read-only blueprints:
docker images
# Output: ubuntu   latest   a1b2c3d4e5f6   72MB

# 4. THE CONTAINER: We tell the Daemon to run the read-only image 
# as an active, isolated computer process
docker run -it ubuntu /bin/bash
# (You are now 'inside' an isolated Ubuntu sandbox running on Windows!)
```

---

### Steps
1. Familiarize yourself with the distinction between Client (Terminal) and Daemon (The Engine).
2. Browse Docker Hub (The Registry) to see official Images (Node, Postgres, Redis).
3. Try pulling a public image.
4. Run it to turn it into an active Container.

---

### Integration

* **React/Next/Node:** You will write your React/Node code on your local system. You will use the Docker Client to tell the Daemon to package your specific codebase into a private Image. You will then push that private Image to a private Registry (like AWS ECR). Your production server will pull it and run the Container!
* **Full-stack apps:** The Daemon manages the internal network, allowing the separate Node.js container to talk securely to the MongoDB container without exposing the database to the outside world.

---

### Impact
This specific architecture ensures security and modularity. The Daemon securely abstracts kernel virtualization, while Docker Hub serves as an incredible open-source library where developers can access pre-configured tech stacks (like an entire WordPress site) in seconds.

---

### Interview Questions
1. **Explain the Docker Client-Server architecture.**
   *Answer: The developer uses the Docker Client (CLI) to send commands via REST API to the Docker Daemon, which natively manages Images, Networks, and Containers on the host OS.*
2. **What is a Docker Registry?**
   *Answer: A hosted storage service (e.g., Docker Hub, AWS ECR) where built Docker Images are pushed, stored, and pulled from.*
3. **What happens if the Docker Daemon goes down?**
   *Answer: The Client loses its connection and cannot execute commands, and any actively running containers may stop functioning or lose network access depending on the restart policy.*

---

### Summary
* **Client:** Terminal commands.
* **Daemon:** The hidden engine doing the actual work.
* **Registry:** Cloud storage for Images.
* **Image:** The blueprint.
* **Container:** The running app.

---
Prev : [01_fundamentals_of_docker.md](./01_fundamentals_of_docker.md) | Next : [03_core_concepts_images_containers.md](./03_core_concepts_images_containers.md)
