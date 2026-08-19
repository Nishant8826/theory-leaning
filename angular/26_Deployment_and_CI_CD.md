# Deployment and CI/CD

## What is it?
**Deployment** is the process of compiling an Angular application into optimized static assets and hosting them on public web servers or cloud platforms (such as AWS S3/CloudFront, Azure Static Web Apps, Firebase Hosting, Vercel, or custom Nginx VPS instances). 

**CI/CD (Continuous Integration / Continuous Deployment)** is the automated pipeline methodology that automatically runs unit tests, verifies code quality, compiles production bundles, and deploys releases to target cloud environments whenever new code is merged.

## Why do we need it?
Manually compiling code, running tests, and SSHing into web servers to copy build artifacts by hand is slow, error-prone, and risky. 

Automated CI/CD pipelines eliminate human error, guarantee that only tested and verified code reaches production, ensure consistent build environments, and enable automated zero-downtime releases.

```
CI/CD Automated Release Pipeline:
Developer pushes code ──> GitHub Actions / GitLab CI 
                      ──> Runs npm run test (Headless Chrome / Jest) 
                      ──> Compiles production bundle with AOT & tree-shaking (esbuild)
                      ──> Builds multi-stage Docker image 
                      ──> Pushes image to container registry (AWS ECR / Docker Hub) 
                      ──> Deploys to cloud cluster (AWS ECS / Kubernetes / Nginx)
```

## How does it work?
1. **Ahead-of-Time (AOT) Compilation (`ng build`)**: Converts TypeScript and Angular templates into highly optimized, minified JavaScript and CSS files, applying tree-shaking to eliminate unused code.
2. **Static Web Server Hosting**: The compiled `dist/` artifacts are pure static files (HTML, CSS, JS, images) served by high-performance web servers such as Nginx, Apache, or global Content Delivery Networks (CDNs).
3. **Nginx SPA Fallback (`try_files`)**: In Single Page Applications, routing happens client-side in the browser. When a user directly visits or refreshes a nested URL (e.g., `/dashboard/analytics`), the web server must be configured to fall back to `index.html` (`try_files $uri $uri/ /index.html;`) so that the Angular Router can handle the path.
4. **CI/CD Pipeline Configurations**: YAML workflow files (e.g., `.github/workflows/deploy.yml`) specify the automated steps for checking out code, installing locked dependencies (`npm ci`), executing test suites, and pushing build artifacts to production.

## Impact
* **Application Architecture**: Establishes predictable environment configurations, automated asset distribution, and repeatable build artifacts.
* **Performance**: Modern esbuild production compilation delivers deep tree-shaking, automated cache-busting hashing, and Gzip/Brotli compression support.
* **Maintainability**: Automated test execution in CI prevents regression bugs from reaching production environments.

## Real World Example
In a high-scale enterprise application, when a developer merges a pull request into the `main` branch, a GitHub Actions workflow automatically triggers:
1. It installs dependencies using `npm ci`.
2. It executes all unit tests (`npm run test -- --watch=false`).
3. It builds the production bundle and packages it into a lightweight Nginx Docker container.
4. It rolls out the new container to a production Kubernetes cluster with zero downtime.

## Syntax
* **Production Build Command**: `ng build --configuration production`
* **Reading Environment Variables**:
```typescript
import { environment } from '../environments/environment';

console.log('Active Backend API:', environment.apiUrl);
```

## Code Examples
Below is a complete enterprise deployment setup featuring a **Multi-Stage Dockerfile**, an **Nginx SPA configuration**, and a **GitHub Actions CI/CD pipeline**:

### `Dockerfile` (Multi-Stage Production Build)
```dockerfile
# Stage 1: Build the Angular Application
FROM node:20-alpine AS build-stage
WORKDIR /app

# Copy dependency manifests and install exact locked packages
COPY package*.json ./
RUN npm ci

# Copy full application source and compile for production
COPY . .
RUN npm run build -- --configuration=production

# Stage 2: Serve Static Assets with Lightweight Nginx
FROM nginx:alpine

# Copy compiled static assets from build stage to Nginx web root
COPY --from=build-stage /app/dist/my-app/browser /usr/share/nginx/html

# Copy custom Nginx configuration for SPA routing fallback
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### `nginx.conf` (SPA Routing & Static Caching)
```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        # Essential SPA rule: Redirect all missing file requests to index.html
        try_files $uri $uri/ /index.html;
    }

    # Enable long-term aggressive caching for hashed static assets
    location ~* \.(?:ico|css|js|gif|jpe?g|png|woff2?|svg)$ {
        root /usr/share/nginx/html;
        expires 1y;
        add_header Cache-Control "public, max-age=31536000, immutable";
    }

    # Ensure index.html is never cached aggressively
    location = /index.html {
        root /usr/share/nginx/html;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }
}
```

### `.github/workflows/deploy.yml` (GitHub Actions CI/CD Pipeline)
```yaml
name: Production Deployment Pipeline

on:
  push:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Source Code
        uses: actions/checkout@v4

      - name: Setup Node.js Runtime
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install Locked Dependencies
        run: npm ci

      - name: Execute Automated Unit Tests
        run: npm run test -- --watch=false --browsers=ChromeHeadless

      - name: Compile Production Build
        run: npm run build -- --configuration=production

      # Cloud deployment step (e.g., deploying to AWS S3/CloudFront)
      # - name: Deploy to Cloud
      #   run: aws s3 sync ./dist/my-app/browser s3://my-production-bucket --delete
```

## Best Practices
1. **Never Hardcode API Endpoints**: Store environment-specific configuration values (API URLs, logging levels, public keys) inside `src/environments/environment.ts` and `environment.production.ts`.
2. **Use Multi-Stage Docker Builds**: Build your application in a dedicated Node.js build container and copy only the final static `dist/` files into a minimal Alpine Nginx image. This reduces image size from ~1GB down to ~25MB and prevents build tooling from leaking into production.
3. **Configure Nginx `try_files` for SPAs**: Always include `try_files $uri $uri/ /index.html;` in web server configurations to ensure direct navigation and page reloads work seamlessly with client-side routing.
4. **Set Correct Cache-Control Headers**: Set `immutable` long-term caching for hashed JS/CSS assets, but set `no-cache` for `index.html` so users receive updates immediately upon new deployments.

## Common Mistakes
* **Deploying Un-minified Development Builds**: Deploying without `--configuration production`, resulting in massive bundle sizes containing debug metadata and development source maps.
* **Missing SPA Rewrite Rules**: Forgetting the `try_files` directive on Nginx or Apache. When users refresh a sub-route like `/admin/users`, the server returns a `404 Not Found` error because no physical `users` file or directory exists on the disk.

## Interview Questions & Answers
### Q: Why do Single Page Applications (SPAs) require custom server rewrite rules (such as Nginx's `try_files`)?
**A**: In SPAs, routing is managed client-side by JavaScript (`Angular Router`). When a user visits `/products/42` and refreshes the browser, the web server looks for a physical directory or file named `/products/42`. Because that file does not exist on disk, the server returns a `404 Not Found`. Configuring `try_files $uri $uri/ /index.html;` instructs the server to serve `index.html` whenever a static file is not found, allowing Angular Router to read the URL path and render the correct component in the browser.

### Q: What are the key advantages of Multi-Stage Docker builds in Angular deployments?
**A**: Multi-Stage Docker builds separate the build environment from the runtime environment. The first stage uses a full Node.js image with build tools and dependencies to compile the Angular code. The second stage uses a lightweight Nginx web server image and copies only the compiled static output (`dist/`). This produces an ultra-small, secure production image (~25MB) with no Node.js runtime overhead, faster startup times, and a drastically reduced security attack surface.

## Summary
Deployment bundles Angular applications into optimized static assets for production hosting. CI/CD pipelines automate testing, building, containerization, and cloud delivery. Proper web server configuration (such as Nginx `try_files` and cache-control headers) guarantees smooth client-side routing and optimal loading speeds across global CDNs.

---

Previous : [Enterprise Architecture](./25_Enterprise_Architecture.md) | Index : [Home](./00_index.md) | Next : —
