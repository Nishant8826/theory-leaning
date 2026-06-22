# Deployment and CI/CD

## What is it?
Deployment is the process of building, packaging, and hosting an Angular application on web servers. CI/CD (Continuous Integration and Continuous Deployment) is the practice of automating code builds, test executions, and server deployments whenever changes are pushed to repository branches.

## Why do we need it?
Building production code manually on local developer machines and uploading files to servers (e.g. via FTP) is slow and prone to errors. Developers can deploy incorrect configurations, skip running unit tests, or run compilation tasks incorrectly. CI/CD pipelines automate building, testing, and deployment to staging or production environments, ensuring consistent, secure releases.

```
CI/CD Pipeline:
Developer pushes code ──> GitHub Actions triggers ──> Installs dependencies (npm ci)
                       ──> Runs tests (ng test) ──> Compiles assets (ng build --configuration=production)
                       ──> Packages into Docker container ──> Deploys to cloud hosts (AWS/Azure/Firebase)
```

## How does it work?
1. **Production Build (`ng build`)**: Compiles TypeScript and templates into highly optimized, minified HTML, CSS, and JS files. Bypasses dev servers and applies deep tree-shaking to keep file sizes small.
2. **Environment Files**: Configure variables (like API URLs) for different environments (e.g., `environment.ts` for development and `environment.prod.ts` for production).
3. **Nginx Routing Rules**: Configures web servers to direct all incoming URLs back to `index.html` to support client-side routing.
4. **Dockerization**: Packages the compiled application along with a web server (like Nginx) inside a container, ensuring it runs consistently across environments.

## Impact
* **Application Architecture**: Directs how dynamic configuration files and API URLs are managed across environments.
* **Performance**: Production builds minimize bundle sizes, resulting in faster load times.
* **Maintainability**: Automated deployments ensure that code passes all test assertions before entering production.

## Real World Example
An enterprise development team uses GitHub Actions to automate their releases. When a developer merges code into the `main` branch, the pipeline automatically runs tests, builds production assets, builds a Docker image, and deploys it to AWS ECS within minutes.

## Syntax
* **Building for Production**: `ng build --configuration production`
* **Local environment config read**:
```typescript
import { environment } from '../environments/environment';
console.log(environment.apiUrl);
```

## Hinglish Explanation

CI/CD aur Deployment ka matlab hai **"Apne local code ko automatic test aur compile karke cloud web servers par launch karna"**. CI/CD aur Deployment ke teen core concepts hain:

### 1. Production Build (`ng build`)
* Local system me running code lightweight files format me nahi hota. Build commands (jaise `npm run build -- --configuration=production`) chalanse se Angular code ko compress, optimize aur AOT (Ahead-of-Time) compile karke static files me generate karta hai.

### 2. Nginx Server configuration (Routing redirection)
* Single Page Application me saari logic single `index.html` file ke zariye chalti hai. Router link switch (jaise `/dashboard`, `/settings`) server par directly register nahi hote.
* Nginx web server par is framework ko serve karne ke liye configuration settings me rewrite rules `try_files $uri /index.html` likhna mandatory hai, warna direct URL access karne par users ko screen par 404 file error show hogi.

### 3. Automated Pipelines (CI/CD)
* Code updates ko cloud servers (jaise AWS, Firebase, netlify) par publish karne se pehle GitHub Actions pipelines automatic execute hoti hain jo static build compilation checks aur Unit test verification automate karti hain.

## Code Examples
Below is an implementation of a **Docker multi-stage configuration**, an **Nginx routing rule**, and a **GitHub Actions CI/CD pipeline**.

### `Dockerfile` (Multi-stage build configuration)
```dockerfile
# Stage 1: Build the Angular application
FROM node:18-alpine AS build-stage
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build -- --configuration=production

# Stage 2: Serve the application using Nginx
FROM nginx:alpine
# Copy compiled static assets from Stage 1
COPY --from=build-stage /app/dist/my-app/browser /usr/share/nginx/html
# Copy custom Nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### `nginx.conf` (Nginx client-side routing fallback)
```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        # Essential rule: Redirect all missing static routes to index.html
        try_files $uri $uri/ /index.html;
    }

    # Cache configurations for static files
    location ~* \.(?:ico|css|js|gif|jpe?g|png)$ {
        root /usr/share/nginx/html;
        expires 1y;
        add_header Cache-Control "public, must-revalidate";
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
```

### `.github/workflows/deploy.yml` (GitHub Actions workflow file)
```yaml
name: CI/CD Production Build

on:
  push:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Source Code
        uses: actions/checkout@v3

      - name: Setup Node.js Environment
        uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: 'npm'

      - name: Install Dependencies
        run: npm ci

      - name: Run Unit Tests
        run: npm run test -- --watch=false --browsers=ChromeHeadless

      - name: Build Production Assets
        run: npm run build -- --configuration=production

      # Optional deploy steps can follow (e.g. deploying to AWS S3, Firebase, etc.)
```
## Best Practices
1. **Never Hardcode API URLs**: Use environment files to store API configurations, and read them dynamically in your services.
2. **Use Multi-Stage Docker Builds**: Use multi-stage Docker builds to compile assets in a build image and copy them to a clean Nginx image, keeping production image sizes small.
3. **Configure Nginx try_files**: Always configure Nginx's `try_files` rule to redirect missing routes to `index.html`. This ensures client-side routing works when users refresh URLs.

## Common Mistakes
* **Including development code in production**: Deploying development builds to production, which includes debugging code and source maps, increasing bundle sizes. Always use `--configuration production`.
* **Missing server redirection rules**: Deploying to Nginx without a fallback rewrite rule. When users refresh nested paths (like `/dashboard/profile`), Nginx will return a `404 Not Found` error.

## Interview Questions & Answers
### Q: Why do we need custom web server configurations (like Nginx's try_files) when deploying Single Page Applications?
**A**: We need them because SPAs use client-side routing. Since paths (like `/products/12`) only exist in the client-side JavaScript bundle and not on the server, refreshing the page will cause the server to return a `404 Not Found` error. Configuring a fallback rule (like `try_files $uri /index.html`) instructs the server to serve `index.html` for all unmatched paths, allowing the client-side router to handle the route.
* **Hinglish Explanation**: Single Page Applications (SPAs) me client-side routing use hoti hai (matlab urls browser javascript me switch hoti hain, actual server par wo files physical exist nahi kartin). Jab user `/products/12` URL par page refresh karta hai, toh web server (jaise Nginx) us file ko dhundhta hai aur na milne par `404 Not Found` error de deta hai. Isliye server par `try_files $uri /index.html` configure karna zaroori hai, jo server ko kehta hai ki unmatched links par bhi `/index.html` file load kare, taaki Angular Router us path ko interpret kar sake.

### Q: What is the benefit of using multi-stage Docker builds?
**A**: Multi-stage builds compile applications inside a build image and copy the static assets to a clean web server image, keeping the production image thin. This keeps image sizes small, accelerates deployments, and avoids exposing source files in production.
* **Hinglish Explanation**: Multi-stage Docker builds se production image size bohot chota aur clean rehta hai. Pehli stage (build stage) me hum heavy Node.js tools aur dependencies load karke application compile karte hain, aur doosri stage (production stage) me sirf final compiled static files (dist folder) ko lightweight Nginx container me copy kar dete hain. Isse main source files compile history secure rehti hai aur server launch fast hota hai.

## Summary
Deployment builds and packages static assets for web servers, while CI/CD pipelines automate testing and releases. Configuring web servers (like Nginx) to support client-side routing ensures smooth deployments to cloud hosts.

---

Previous : [Enterprise Architecture](./25_Enterprise_Architecture.md) | Index : [Home](./00_index.md) | Next : [Real World E-Commerce Project](./27_Real_World_ECommerce_Project.md)
