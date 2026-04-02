# Debugging Containers & Best Practices

---

### What
- **Debugging:** Investigating crashing loops, connection failures, and memory errors inside headless Linux containers.
- **Best Practices:** Writing structured Dockerfiles efficiently, optimizing images, and ensuring secure production rollouts.

---

### Why
When bugs arise, developers often panic because they don't have a visual UI. Identifying specific terminal commands mitigates this frustration and resolves errors natively and dynamically. Streamlining architecture using best practices saves massive amounts of cloud bills and build times.

---

### How
- Inspect executing containers utilizing `docker logs` and `docker exec`.
- Implement Layer Caching heavily.
- Maintain the principle of one main task/process per container!

---

### Implementation

Master the exact debugging methodology intuitively:

**The Golden Debugging Flow:**
1. *Is the box currently running?* $\rightarrow$ `docker ps` or `docker ps -a` 
2. *Why did it crash?* $\rightarrow$ `docker logs [container_ID]`
3. *Are files incorrectly configured physically inside?* $\rightarrow$ `docker exec -it [container_ID] /bin/sh`
4. *Did environment variables transfer correctly?* $\rightarrow$ `docker inspect [container_ID]`

**Dockerfile Best Practices:**
*  **Use Official Verified Images:** Use `node:18-alpine` instead of maintaining your own complex Ubuntu image.
*  **Order matters heavily:** Organize `COPY package.json` prior to copying your code to prevent redundant installations.
*  **One concern per container:** Don't attempt to run a MongoDB database AND a Node.js server inside the same container. Split them using Docker Compose!

---

### Steps (Scenario: DB connection fails in Node.js)
1. Read stack errors via `docker logs my_node_app` (Look for "ECONNREFUSED").
2. Check if the database process crashed via `docker ps -a`.
3. Enter the Node container interactively using `docker exec -it my_node_app /bin/sh`. 
4. Run `ping db` to verify internal DNS networking logic cleanly.

---

### Integration

* **React/Next.js/Node.js:** Ensure that your Javascript `console.error` logs actually print to the standard output cleanly, so Docker's logging daemon catches the errors securely instead of silencing them.

---

### Impact
Adhering to these best practices executing efficiently mitigates complete architecture failures, inherently saving debugging effort proactively proactively natively executing successfully perfectly.

---

### Interview Questions
1. **Your Node.js container starts successfully, but crashes 5 seconds later. How do you troubleshoot?**
   *Answer: Initially run `docker logs <container>` to examine the application's terminal output. If insufficient, use `docker inspect` to verify injected variables, or investigate if it's running out of RAM.*
2. **What occurs if you place `COPY . .` prior to `RUN npm install`?**
   *Answer: It breaks Docker's dependency caching mechanism. Any small change to your codebase will alter the layer hash, forcing Docker to painstakingly re-download all npm modules from scratch on every build.*
3. **Why should you never run multiple major processes (like Nginx and MySQL) inside one container?**
   *Answer: It defeats the purpose of containerization. Containers should be ephemeral, scaling independently. If MySQL crashes, it shouldn't take down the web server along with it.*

---

### Summary
* Master the native usage of `ps`, `logs`, and `exec`.
* Layer instructions accurately minimizing execution times via caching.
* Separate major explicit concerns functionally utilizing multiple containers securely.

---
Prev : [13_deployment_and_ci_cd.md](./13_deployment_and_ci_cd.md) | Next : [15_interview_preparation.md](./15_interview_preparation.md)
