# Dockerizing React and Next.js Frontends

---

### What
Dockerizing a frontend application changes significantly based on whether it is a strictly client-side Single Page Application (like plain React/Vite) or a Server-Side Rendered application (like Next.js).
- **React (Vite/CRA):** Needs to be built into static HTML/CSS files, which are then served/hosted by a lightning-fast web server like Nginx.
- **Next.js:** Next.js possesses its own internal Node server to handle server-side logic and API routes, so it stays entirely in the Node container ecosystem instead of Nginx.

---

### Why
Deploying frontends via Docker guarantees consistent routing behaviors and environmental variables regardless of where they are hosted. 

---

### How
For Next.js, the Dockerfile looks shockingly similar to a standard Node.js backend Dockerfile, because Next is fundamentally a Node server process. We copy standard files, run the build command, and start the Next server.

---

### Implementation

Here is a robust Dockerfile explicitly mapped for a **Next.js** application.

```dockerfile
# File: Dockerfile (Inside Next.js project folder)

FROM node:18-alpine

WORKDIR /app

# Copy dependency packages
COPY package*.json ./

# Install Node dependencies
RUN npm install

# Copy the rest of the Next.js files (pages, components, public)
COPY . .

# Build the heavy production optimized Next.js bundle (.next folder)
RUN npm run build

EXPOSE 3000

# Trigger the Next.js internal server
CMD ["npm", "start"]
```

---

### Steps (If deploying standard regular React/Vite)
If you are NOT using Next, but instead using purely Vite/React static apps, running a Node server to host simple HTML files is a massive waste of RAM. Instead, you build the image using Multi-Stage Builds:
1. Stage 1 (Node): Copy files, run `npm install`, and run `npm run build`. This generates a lightweight `dist/` folder.
2. Stage 2 (Nginx): Use an Nginx image, grab the `dist/` folder from Stage 1, and let Nginx serve it with sub-millisecond response times natively over port 80.

---

### Integration

* **React/Next.js and Env Variables:** When dockerizing Next.js, remember that anything prefixed with `NEXT_PUBLIC_` gets physically baked into the Javascript HTML bundles during the `RUN npm run build` phase. If you change a generic env variable later on your production server without rebuilding the Docker Next.js image, the frontend will not see the change! Next.js bake-ins happen at *build time*, not *run time*.
* **Full-stack apps:** Add your newly dockerized Next.js image to the `frontend` service in your master `docker-compose.yml`.

---

### Impact
Dockerized frontends scale perfectly in orchestrators like Kubernetes. If a massive traffic spike hits your Next.js e-commerce app on Black Friday, Docker can clone identical frontend containers simultaneously across distinct cloud servers effortlessly to absorb the hit.

---

### Interview Questions
1. **Why is a Node.js container needed for a Next.js application, but NOT for a client-side Vite React application in production?**
   *Answer: Because Next.js has server-sided functionality (SSR, API routes) requiring a dedicated active Node runtime. A Vite React app generates static HTML/JS artifacts which are best served via highly-optimized web servers like Nginx, requiring zero active Node.js processes.*
2. **What is the risk of utilizing Environment Variables during a Next.js Docker Build Phase?**
   *Answer: Environment variables that are rendered dynamically onto the front-end (public prefixes) are permanently injected statically into the compiled chunks during `npm build`. Altering container variables dynamically at runtime will have zero logical effect on the already compiled frontend bundle.*

---

### Summary
* Next.js utilizes a standard Node Container (Build -> NPM Start).
* Client-Side React uses structural artifacts served by Nginx.
* Be heavily cautious about when environments build themselves statically!

---
Prev : [09_dockerizing_nodejs_backend.md](./09_dockerizing_nodejs_backend.md) | Next : [11_advanced_multistage_builds.md](./11_advanced_multistage_builds.md)
