# 10 – Deployment in Next.js

---

## What is Deployment?

Deployment is the process of taking your app from your local machine and putting it on the **internet** so anyone in the world can access it.

```
Development (localhost:3000)  →  Deployment  →  Production (yourdomain.com)
   Only YOU can see it              ↑              Everyone can see it
                              Build + Deploy
```

---

## Why Does Deployment Matter?

| Concern | Why It's Important |
|---------|-------------------|
| **Availability** | Your app must be accessible 24/7 |
| **Performance** | Production builds are optimized (minified, compressed) |
| **Scaling** | Handle thousands of users, not just your laptop |
| **Security** | HTTPS, environment variables, access controls |
| **CI/CD** | Auto-deploy on every git push |

---

## How Deployment Works in Next.js

### Step 1: Build Your App

```bash
npm run build
```

This creates an optimized production bundle in the `.next/` folder:
- JavaScript is minified and tree-shaken
- CSS is optimized
- Static pages are pre-rendered
- Images are optimized

### Step 2: Start Production Server

```bash
npm run start
```

This starts a Node.js server serving the optimized build.

### Step 3: Deploy to a Hosting Platform

---

## Deployment Options

### 1. Vercel (Recommended — Built by Next.js Team)

**What:** The easiest way to deploy Next.js. Built by the same team that created Next.js.

**Why:**
- Zero-config deployment
- Automatic HTTPS
- Global CDN (Edge network)
- Preview deployments for every pull request
- Built-in analytics

**How:**

```bash
# Method 1: CLI
npm install -g vercel
vercel

# Method 2: Connect GitHub repo
# 1. Go to vercel.com
# 2. Import your GitHub repository
# 3. Vercel auto-detects Next.js and deploys
# 4. Every git push auto-deploys
```

**Real-world Example:** Most Next.js startups use Vercel for deployment because it handles scaling, SSL, and CDN automatically.

### 2. AWS (EC2 / Amplify / Lambda)

**What:** Self-hosted deployment on Amazon Web Services.

**Why:** Full control over infrastructure, compliance requirements, or existing AWS setup.

```bash
# EC2 Deployment (Manual)
# 1. Launch an EC2 instance
# 2. SSH into the server
# 3. Install Node.js
# 4. Clone your repo
# 5. npm install && npm run build
# 6. npm run start
# 7. Use PM2 to keep it running
# 8. Set up Nginx as reverse proxy

# PM2 Process Manager
npm install -g pm2
pm2 start npm --name "my-app" -- start
pm2 save
pm2 startup
```

### 3. Docker

**What:** Containerize your Next.js app for consistent deployment anywhere.

```dockerfile
# Dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/public ./public

EXPOSE 3000
CMD ["npm", "start"]
```

```bash
# Build and run
docker build -t my-next-app .
docker run -p 3000:3000 my-next-app
```

### 4. Static Export (No Server Needed)

**What:** Export your entire app as static HTML files. No Node.js server required.

**Why:** Deploy to any static hosting (GitHub Pages, S3, Netlify).

```jsx
// next.config.js
const nextConfig = {
  output: 'export',   // Enable static export
};
module.exports = nextConfig;
```

```bash
npm run build
# Output is in the 'out/' folder — pure HTML/CSS/JS
# Upload to any static hosting
```

**Limitation:** No SSR, API routes, or dynamic routes without `generateStaticParams()`.

---

## ⭐ Most Important Concepts

### 1. Environment Variables

**Never hardcode secrets** in your code. Use `.env` files.

```bash
# .env.local (for local development — NOT committed to git)
DATABASE_URL=mongodb://localhost:27017/myapp
NEXT_PUBLIC_API_URL=https://api.example.com
SECRET_KEY=my-super-secret-key
GOOGLE_CLIENT_ID=123456.apps.googleusercontent.com
```

**Critical Rule:**

| Prefix | Accessible Where | Use For |
|--------|-----------------|---------|
| `NEXT_PUBLIC_` | Both server AND client (browser) | Public API URLs, Google Analytics ID |
| No prefix | Server ONLY | Database URLs, API keys, secrets |

```jsx
// ✅ Server Component — can access ALL env vars
const dbUrl = process.env.DATABASE_URL; // Works

// ❌ Client Component — can ONLY access NEXT_PUBLIC_ vars
const secret = process.env.SECRET_KEY; // undefined!
const apiUrl = process.env.NEXT_PUBLIC_API_URL; // Works
```

**On deployment platforms (Vercel, AWS):** Set environment variables in the dashboard, not in `.env` files.

### 2. Build Output Analysis

```bash
npm run build
```

```
Route (app)                              Size     First Load JS
┌ ○ /                                    5.2 kB        87 kB
├ ○ /about                               1.1 kB        83 kB
├ ● /blog/[slug]                         3.4 kB        85 kB
├ λ /dashboard                           8.7 kB        91 kB
└ λ /api/products                        0 B            0 B

○  Static   (pre-rendered at build time)
●  SSG      (generated with data at build time)
λ  Dynamic  (rendered on every request)
```

| Symbol | Meaning | Performance |
|--------|---------|-------------|
| ○ | Static page (no data) | Fastest |
| ● | SSG (data at build time) | Fast |
| λ | Dynamic / SSR | Slower (server work per request) |

### 3. CI/CD Pipeline

```
Developer pushes code to GitHub
        ↓
CI/CD pipeline triggers automatically
        ↓
1. Install dependencies (npm ci)
2. Run linting (npm run lint)
3. Run tests (npm test)
4. Build (npm run build)
5. Deploy to staging/production
        ↓
Users see the updated app
```

### 4. Preview Deployments

On platforms like Vercel, every Pull Request gets its own unique URL:

```
main branch     → https://myapp.vercel.app (Production)
feature-branch  → https://myapp-git-feature-branch.vercel.app (Preview)
```

**Impact:** QA reviewers and teammates can test changes on a live URL before merging. No "it works on my machine" issues.

---

## Deployment Comparison Table

| Platform | Difficulty | Cost | Best For |
|----------|-----------|------|----------|
| **Vercel** | ⭐ Easiest | Free tier + paid | Most Next.js projects |
| **Netlify** | Easy | Free tier + paid | Static sites, simple apps |
| **AWS (EC2)** | Hard | Pay per use | Full control, enterprise |
| **AWS (Amplify)** | Medium | Pay per use | AWS-integrated projects |
| **Docker** | Medium | Depends on hosting | Consistent environments |
| **Railway** | Easy | Free tier + paid | Full-stack apps |
| **DigitalOcean** | Medium | $4–12/month | Budget-friendly |
| **Static Export** | Easy | Free (S3, GitHub Pages) | No server features needed |

---

## Interview Questions & Answers

### Q1: How do you deploy a Next.js application?
**Answer:** The easiest method is deploying to Vercel — connect your GitHub repo and every push auto-deploys. For self-hosting: run `npm run build` to create the production bundle, then `npm run start` to start the Node.js server. You can also use Docker, AWS, or export as static files.

### Q2: What is the difference between `npm run dev` and `npm run build && npm run start`?
**Answer:** `dev` runs a development server with hot reload, error overlays, and no optimizations — meant for development only. `build` creates an optimized production bundle (minified JS, pre-rendered pages), and `start` serves that bundle. Production mode is significantly faster and smaller.

### Q3: What are environment variables and how do they work in Next.js?
**Answer:** Environment variables store configuration like API keys and database URLs outside your code. In Next.js, variables prefixed with `NEXT_PUBLIC_` are available in both server and client code. Variables without the prefix are only available on the server (for security). Store them in `.env.local` locally and in the platform's dashboard for production.

### Q4: What is static export in Next.js?
**Answer:** Setting `output: 'export'` in `next.config.js` generates pure HTML/CSS/JS files that can be hosted on any static hosting (S3, GitHub Pages, etc.). No Node.js server needed. However, this disables SSR, API routes, and other server-dependent features.

### Q5: What do the symbols ○, ●, and λ mean in the build output?
**Answer:** ○ = Static page (no data, fastest). ● = SSG page (data fetched at build time). λ = Dynamic/SSR page (server renders on each request). Aim to have as many ○ and ● pages as possible for best performance.

### Q6 (Scenario): Your app crashes in production but works fine in development. What could be wrong?
**Answer:** Common causes: (1) Missing environment variables on the production server, (2) Using browser-only APIs (`window`, `document`) in Server Components, (3) Development mode hides certain errors that build mode catches, (4) Different Node.js versions between local and production.

### Q7 (Scenario): Your marketing team wants to preview changes before they go live. How do you set this up?
**Answer:** Use Preview Deployments on Vercel. Every Pull Request automatically gets a unique preview URL. The marketing team can review changes on this live URL before approving the merge. This is available out of the box with Vercel's GitHub integration.

---

### 🔗 Navigation
- ⬅️ Previous: [09_SEO.md](./09_SEO.md)
- ➡️ Next: [11_App_Router.md](./11_App_Router.md)
