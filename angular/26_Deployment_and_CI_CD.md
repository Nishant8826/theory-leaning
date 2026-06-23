# Deployment and CI/CD

## What is it?
Deployment local application codebase ko build karke public web servers (jaise AWS, Azure, Firebase, ya custom VPS) par host karne ka process hai. CI/CD (Continuous Integration / Continuous Deployment) pipelines automations frameworks hain jo build testing, code compilation checks, assets distribution, aur cloud updates releases ko automate karte hain.

## Why do we need it?
Manually code templates compile karna, styles minification apply karna, aur file directories ko server engine (Nginx) locations par hand-copy karna slow execution aur error-prone pipeline systems banata hai. Automated pipelines aur standard server layouts use karne se human errors terminate ho jate hain, releases delivery fast ho jati hai, aur client compatibility issues resolve ho jate hain.

```
CI/CD Pipeline:
Developer pushes code ──> GitHub Actions ──> Runs npm run test ──> Builds production assets (esbuild)
                       ──> Builds Docker Image ──> Pushes to AWS ECR ──> Updates web server (Zero Downtime)
```

## How does it work?
1. **Production Compilation (`ng build`)**: Production build script typescript code ko Ahead-of-Time (AOT) compile karke optimized, minified HTML, CSS, aur static JS files generate karta hai.
2. **Web Server Hosting**: Generated static assets ko Nginx ya Apache jaise HTTP web servers par host kiya jata hai.
3. **Nginx Redirection**: Single Page Applications (SPAs) me routing client-side par hoti hai. Agar user page refresh kare, toh web server 404 throw kar sakta hai. Ise resolve karne ke liye Nginx me redirection rule `try_files $uri /index.html` apply kiya jata hai.
4. **CI/CD Configuration**: Workflow config files (jaise GitHub Actions yaml files) define karte hain ki codebase changes par kaise building, testing, aur deployment trigger honge.

## Impact
* **Application Architecture**: Clear build commands, server redirections, aur automated deployments setups.
* **Performance**: esbuild compiling process tree-shaking perform karke production code bundle size minimize rakhta hai.
* **Maintainability**: Automated deployments aur unit test runs ensure karte hain ki code production me jaane se pehle saare test assertions ko pass kare.

## Real World Example
Ek enterprise development team releases ko automate karne ke liye GitHub Actions ka use karti hai. Jab koi developer code ko `main` branch me merge karta hai, toh pipeline automatically tests run karti hai, production assets build karti hai, ek Docker image generate karti hai, aur use kuch hi minutes me AWS ECS par deploy kar deti hai.

## Syntax
* **Building for Production**: `ng build --configuration production`
* **Local environment config read**:
```typescript
import { environment } from '../environments/environment';
console.log(environment.apiUrl);
```

## Code Examples
Neeche **Docker multi-stage configuration**, **Nginx routing rule**, aur **GitHub Actions CI/CD pipeline** ka implementation diya gaya hai.

### `Dockerfile`
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

### `nginx.conf`
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
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
}
```

### `.github/workflows/deploy.yml`
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
1. **Never Hardcode API URLs**: Environment files ka use karein API configurations store karne ke liye, aur unhe services me dynamically read karein.
2. **Use Multi-Stage Docker Builds**: Multi-stage Docker builds ka use karein compile stage me heavy tools use karne aur dynamic clean image me copy assets generate karne ke liye, taaki production image size minimum rahe.
3. **Configure Nginx try_files**: Nginx ke `try_files` rule ko hamesha configure karein taaki unmatched routes `index.html` par fall back karein. Yeh ensure karta hai ki page refresh hone par client-side routing fail na ho.

## Common Mistakes
* **Including development code in production**: Development builds ko production par deploy karna, jisme debugging code aur source maps hote hain aur bundle size bada ho jata hai. Humesha `--configuration production` use karein.
* **Missing server redirection rules**: Nginx par fallback rewrite rule ke bina deploy karna. Jab users nested paths (jaise `/dashboard/profile`) ko refresh karenge, toh Nginx `404 Not Found` error return karega.

## Interview Questions & Answers
### Q: Why do we need custom web server configurations (like Nginx's try_files) when deploying Single Page Applications?
**A**: Single Page Applications (SPAs) me client-side routing use hoti hai (matlab urls browser javascript me switch hoti hain, actual server par wo files physical exist nahi kartin). Jab user `/products/12` URL par page refresh karta hai, toh web server (jaise Nginx) us file ko dhundhta hai aur na milne par `404 Not Found` error de deta hai. Isliye server par `try_files $uri /index.html` configure karna zaroori hai, jo server ko kehta hai ki unmatched links par bhi `/index.html` file load kare, taaki Angular Router us path ko interpret kar sake.

### Q: What is the benefit of using multi-stage Docker builds?
**A**: Multi-stage Docker builds se production image size bohot chota aur clean rehta hai. Pehli stage (build stage) me hum heavy Node.js tools aur dependencies load karke application compile karte hain, aur doosri stage (production stage) me sirf final compiled static files (dist folder) ko lightweight Nginx container me copy kar dete hain. Isse main source files compile history secure rehti hai aur server launch fast hota hai.

## Summary
Deployment static assets ko build aur package karta hai web servers ke liye, jabki CI/CD pipelines testing aur releases ko automate karti hain. Client-side routing ko support karne ke liye web servers (jaise Nginx) ko configure karna cloud hosts par smooth deployment ensure karta hai.

---

Previous : [Enterprise Architecture](./25_Enterprise_Architecture.md) | Index : [Home](./00_index.md) | Next : [None]()
