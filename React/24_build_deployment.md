# 24 - Build & Deployment 🚀


---

## 🤔 What is Building and Deploying?

- **Build** = Converting your React dev code into optimized files a browser can understand (HTML + CSS + JS)
- **Deploy** = Uploading those files to a server so anyone on the internet can visit your app

> **Real-world analogy:**
> **Build** = Baking a cake in the kitchen (development) and boxing it up perfectly (build).
> **Deploy** = Delivering that box to the customer (putting it on a server for users).

---

## 🔄 Development vs Production

| | Development (`npm run dev`) | Production (`npm run build`) |
|---|---|---|
| Speed | Fast refresh | Optimized bundle |
| Code | Raw, readable | Minified, compressed |
| Size | Large | Much smaller |
| Errors | Visible (console) | Hidden from users |
| Source Maps | Yes | Optional |
| Purpose | For developers | For users |

---

## 🏗️ Step 1: Build Your App

```bash
# For Vite
npm run build

# For CRA
npm run build
```

This creates a `dist/` (Vite) or `build/` (CRA) folder with optimized files:

```
dist/
├── index.html          ← Single HTML file
├── assets/
│   ├── index-abc123.js ← All JavaScript (minified)
│   ├── index-xyz789.css← All CSS (minified)
│   └── images/         ← Optimized images
```

---

## 🔍 Preview the Build Locally

Before deploying, test your production build:

```bash
# Vite
npm run preview   # Serves the built files at localhost:4173

# Or use serve (any project)
npm install -g serve
serve dist         # Serves built files
```

---

## 🚀 Deployment Options

### Option 1: Vercel (⭐ Best for React — Free!)

**Easiest option — connects to GitHub and auto-deploys!**

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy (from project root)
vercel
```

Or simply push to GitHub + connect to [vercel.com](https://vercel.com) — it auto-builds and deploys!

**Features:**
- ✅ Auto-deploys on every GitHub push
- ✅ Free SSL certificate
- ✅ Custom domains
- ✅ Preview URLs for every PR
- ✅ Environment variable management

---

### Option 2: Netlify (Also Great — Free!)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Build and deploy
npm run build
netlify deploy --dir=dist --prod
```

Or drag & drop the `dist/` folder at [netlify.com](https://netlify.com)!

**Important for React Router on Netlify:**

Create `public/_redirects` file:
```
# Fix React Router 404 on refresh
/*    /index.html   200
```

---

### Option 3: GitHub Pages (Free, Simple)

```bash
# Install gh-pages
npm install --save-dev gh-pages
```

Add to `package.json`:
```json
{
  "homepage": "https://yourusername.github.io/your-repo",
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d dist"
  }
}
```

```bash
npm run deploy
```

**Note:** For Vite, set the base in `vite.config.js`:
```javascript
export default {
  base: "/your-repo-name/",
}
```

---

### Option 4: Firebase Hosting

```bash
npm install -g firebase-tools
firebase login
firebase init hosting   # Choose dist/ as public directory
npm run build
firebase deploy
```

---

### Platform Comparison

| Platform | Free Tier | Auto Deploy | Custom Domain | Best For |
|---|---|---|---|---|
| Vercel | ✅ Generous | ✅ GitHub | ✅ | React (Recommended) |
| Netlify | ✅ Generous | ✅ GitHub | ✅ | Static sites |
| GitHub Pages | ✅ Unlimited | ✅ With CI | ✅ | Open source projects |
| Firebase | ✅ Limited | ✅ With CI | ✅ | Google ecosystem |
| Render | ✅ Limited | ✅ GitHub | ✅ | Full-stack apps |

---

## ⚙️ CI/CD with GitHub Actions

Automatically build and deploy on every GitHub push:

```yaml
# .github/workflows/deploy.yml
name: Deploy to Vercel

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Install dependencies
        run: npm install

      - name: Build
        run: npm run build
        env:
          VITE_API_URL: ${{ secrets.VITE_API_URL }}

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: "--prod"
```

---

## 🔐 Environment Variables in Production

On Vercel/Netlify, set env vars in the dashboard — NOT in `.env` files committed to GitHub:

```
Vercel Dashboard:
Project Settings → Environment Variables
→ Add: VITE_API_URL = https://api.production.com
→ Add: VITE_GOOGLE_KEY = AIza...
```

---

## 🔧 Pre-Deployment Checklist

Before deploying check these:

- [ ] `npm run build` completes without errors
- [ ] App works with `npm run preview` locally
- [ ] All environment variables are set on hosting platform
- [ ] No hardcoded localhost URLs
- [ ] 404 redirect configured for React Router (`_redirects` on Netlify)
- [ ] Images are optimized
- [ ] Console has no critical errors
- [ ] Tested in multiple browsers

---

## ❌ Common Mistakes / Tips

- ❌ Deploying without testing the build locally first (`npm run preview`)
- ❌ Forgetting to set env variables on the hosting platform
- ❌ Not setting up redirect rules for React Router → 404 on refresh
- ❌ Committing `node_modules/` to git (always add to `.gitignore`)
- ✅ Use Vercel or Netlify — they make deployment as easy as pushing to GitHub
- ✅ Check build output size — if too large, add more lazy loading

---

## 📝 Summary

- `npm run build` → creates optimized production files in `dist/` or `build/`
- Test production build locally with `npm run preview` 
- Best platforms: **Vercel** (easiest for React) and **Netlify**
- Set environment variables on the hosting platform, not in committed files
- Add a `_redirects` file for Netlify to fix React Router 404s
- Setup CI/CD with GitHub Actions for automatic deploys

---

## 🎯 Practice Tasks

1. Run `npm run build` on your project. Check the `dist/` folder — how small is the bundle?
2. Deploy your React app to **Vercel** — connect your GitHub repo and get a live URL!
3. Set your `VITE_API_URL` environment variable in the Vercel dashboard
4. Create a **Netlify** deployment and add the `_redirects` file for React Router support
5. Set up a basic GitHub Actions workflow that runs `npm run build` on every push

---

← Previous: [23_environment_variables.md](23_environment_variables.md) | Next: [25_react_vs_angular_vue.md](25_react_vs_angular_vue.md) →
