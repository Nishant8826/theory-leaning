# CI/CD with GitHub Actions and Docker

## Why This Exists
Building Docker images manually on your laptop, tagging them, and running `docker push` is fine for a side project. But in a professional team, this is slow, prone to human error, and doesn't scale.

**CI/CD (Continuous Integration / Continuous Deployment)** automates this. Every time a developer pushes code to GitHub, automated robots take over. They run tests, build the Docker image, and push it to a registry (like Docker Hub or AWS ECR). This ensures that the code in production is always tested and up to date without any manual intervention.

## Real World Analogy
Think of CI/CD like an **Automated Car Factory**.
- Developers drop off the blueprint (Code) on a conveyor belt (Git push).
- Robots (GitHub Actions) automatically assemble the car, run safety tests (Unit tests), paint it, and put it in a container (Docker image).
- The container is then loaded onto a ship (Docker Hub) ready to be delivered to customers.

## Core Concepts
- **CI (Continuous Integration)**: Automatically building and testing code on every push.
- **CD (Continuous Deployment)**: Automatically deploying the built image to production.
- **GitHub Actions**: GitHub's built-in tool for automation.
- **Workflow**: A YAML file in your repository that defines the automation steps.
- **Docker Registry**: A place to store Docker images (e.g., Docker Hub, AWS ECR).

## Architecture / Flow

```text
[ Developer ]
       │
       ▼ (Git Push)
[ GitHub Repository ]
       │
       ▼ (Triggers)
[ GitHub Actions Runner ]
       │
       ├───► Runs Tests
       │
       ├───► docker build
       │
       └───► docker push
              │
              ▼
[ Docker Hub / Registry ]
```

## Practical Commands
GitHub Actions uses YAML configuration files located in `.github/workflows/`. Here is the core logic written in shell commands that the GitHub robot executes:

```bash
# Login to Docker Hub using secrets
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

# Build and tag
docker build -t myusername/my-app:latest .

# Push to registry
docker push myusername/my-app:latest
```

## Hands-On Exercise
Let's look at a real GitHub Actions workflow file.

1. In your project, create a folder structure: `.github/workflows/`
2. Create a file named `docker-ci.yml`:
   ```yaml
   name: Build and Push Docker Image

   on:
     push:
       branches: [ "main" ]

   jobs:
     build:
       runs-on: ubuntu-latest

       steps:
       - name: Checkout code
         uses: actions/checkout@v4

       - name: Set up Docker Buildx
         uses: docker/setup-buildx-action@v3

       - name: Login to Docker Hub
         uses: docker/login-action@v3
         with:
           username: ${{ secrets.DOCKER_USERNAME }}
           password: ${{ secrets.DOCKER_PASSWORD }}

       - name: Build and push
         uses: docker/build-push-action@v5
         with:
           context: .
           push: true
           tags: ${{ secrets.DOCKER_USERNAME }}/my-app:latest
   ```

## Mini Project
**Task**: Set up the above workflow and link it to Docker Hub.

1. Create a free account on **Docker Hub**.
2. Go to your GitHub repository -> Settings -> Secrets and variables -> Actions.
3. Add two secrets:
   - `DOCKER_USERNAME`: Your Docker Hub username.
   - `DOCKER_PASSWORD`: Your Docker Hub password (or an access token).
4. Push the `docker-ci.yml` file to your `main` branch.
5. Go to the **Actions** tab on GitHub and watch your image being built and pushed automatically!

### Advanced Mini Project: React Portfolio App with CI/CD
**Task**: Deploy a real-world React Portfolio project following production best practices.

#### 1. The Optimized Dockerfile (Multi-Stage)
Create a `Dockerfile` in your React project root. This uses a **Multi-Stage Build** to keep the image small and secure:
```dockerfile
# Stage 1: Build the React Application
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx (Production)
FROM nginx:alpine
# Remove default nginx static files
RUN rm -rf /usr/share/nginx/html/*
# Copy built files from Stage 1
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### 2. The GitHub Actions Workflow
Create `.github/workflows/react-ci.yml`. This includes **Build Caching** to make your builds 10x faster:
```yaml
name: React Portfolio CI/CD

on:
  push:
    branches: [ "main" ]

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Login to Docker Hub
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ secrets.DOCKER_USERNAME }}/react-portfolio:latest
        # Caching layers to speed up builds
        cache-from: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/react-portfolio:buildcache
        cache-to: type=inline
```

#### Real-Time Practices Followed Here:
- **Security**: The final image does **not** contain Node.js or your source code. It only contains Nginx and static files, drastically reducing the attack surface.
- **Scaling**: Frontend apps are stateless. This image can be scaled horizontally to hundreds of instances effortlessly.
- **Volumes**: For production React apps, you do not need volumes for source code. The files are baked into the image. However, you can mount a volume to `/var/log/nginx` if you want to collect logs.

#### How the CI/CD Flow Works (The Story)
Here is what happens every time you push code:
1. **The Trigger**: You push code to the `main` branch (`git push origin main`). GitHub sees this and triggers the workflow.
2. **The Environment**: GitHub spins up a fresh, clean Ubuntu Linux virtual machine in the cloud (the "Runner").
3. **The Steps**:
   - **Checkout**: Downloads your code onto that clean computer.
   - **Setup**: Installs advanced Docker build tools (Buildx).
   - **Login**: Logs in to your Docker Hub account using the secrets you stored.
   - **Build & Push**: Reads your `Dockerfile`, builds the production image, and uploads (pushes) it to Docker Hub automatically!

#### How to Run Locally via Docker
Once your image is on Docker Hub, you can run it locally on any machine with this command:

```bash
docker run -d -p 8081:80 --name my-portfolio rnishant428/react-portfolio:latest
```

**What this does:**
- **`-d`**: Runs the container in the background (detached mode).
- **`-p 8081:80`**: Maps port `8081` on your computer to port `80` inside the container.
- **`--name my-portfolio`**: Gives the container a readable name.
- **`rnishant428/react-portfolio:latest`**: The image to pull and run.

*To view your app, open your browser and go to `http://localhost:8081`.*

## Real Production Usage
- **Semantic Versioning**: In production, instead of just tagging everything as `:latest`, use the Git commit SHA or Git tags (like `:v1.2.0`) so you can roll back to specific versions if something breaks.
- **Security Scanning**: Add steps in your CI/CD pipeline to scan your Docker images for security vulnerabilities (using tools like Trivy or Snyk) before pushing them.

## Common Mistakes
- **Hardcoding Credentials**: Putting your Docker Hub password directly in the YAML file. Anyone who sees your repo can steal it. **Always use GitHub Secrets.**
- **No Cache**: Not using Docker layer caching in CI/CD. This makes builds take 5–10 minutes instead of 30 seconds.

## Debugging Guide
- **Workflow fails at login**: Double check that your GitHub Secrets names match exactly what is in your YAML file.
- **Build fails**: Look at the logs in the GitHub Actions tab. It provides the exact step and error message where the Docker build failed.

## Best Practices
- **Use GitHub Secrets**: For all passwords, tokens, and keys.
- **Multi-stage builds**: Use them to keep the final image pushed to the registry as small as possible.
- **Leverage Cache**: Use `cache-from` and `cache-to` in GitHub Actions to speed up builds.

## Interview Questions
1. **What is the benefit of using CI/CD with Docker?**
   *Answer*: It automates the testing, building, and pushing of images, reducing human error, ensuring consistent builds, and accelerating the release cycle.
2. **How do you keep secrets secure in GitHub Actions?**
   *Answer*: By using GitHub Secrets. You store them in the repository settings and reference them in the YAML file using the `${{ secrets.NAME }}` syntax.

## Summary
CI/CD is the bridge between development and operations. By automating your Docker builds with GitHub Actions, you ensure that high-quality, tested images are always ready for deployment.

---
Prev: [05_scaling_containers.md](./05_scaling_containers.md) | Index: [Index](../00_index.md) | Next: [07_production_deployments_ec2.md](./07_production_deployments_ec2.md)
