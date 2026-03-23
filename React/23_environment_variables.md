# 23 - Environment Variables 🔐

> **Previous: [22_folder_structure.md](./22_folder_structure.md)** | **Next: [24_build_deployment.md](./24_build_deployment.md)**

---

## 🤔 What are Environment Variables?

Environment variables are **configuration values** that change based on where your app is running — development, testing, or production.

> **Real-world analogy:**
> Imagine your office has a **development server** (for testing) and a **production server** (for real users). Your app needs to connect to different databases, APIs, and URLs in each place. Instead of changing code every time, you use environment variables — like a settings file that changes per environment.

---

## ⚠️ Why Not Hardcode API URLs?

```jsx
// ❌ BAD — don't hardcode!
const API_URL = "http://localhost:5000/api"; // Won't work in production!
const API_KEY = "sk-abc123-super-secret-key"; // Exposed in code!
```

```jsx
// ✅ GOOD — use environment variables!
const API_URL = import.meta.env.VITE_API_URL;
const API_KEY = import.meta.env.VITE_API_KEY;
```

---

## 📄 `.env` File Setup

Create a `.env` file in the **root** of your project (next to `package.json`):

```
project/
├── src/
├── public/
├── .env              ← environment variables here
├── .env.local        ← local overrides (not shared)
├── .env.development  ← dev-specific
├── .env.production   ← production-specific
├── package.json
└── vite.config.js
```

---

## 🔑 Vite Environment Variables (Recommended)

**Important:** In Vite, all custom env variables MUST start with `VITE_`

```env
# .env
VITE_API_URL=https://api.myapp.com
VITE_APP_NAME=My React App
VITE_GOOGLE_MAPS_KEY=AIzaSyAbc123...
VITE_FEATURE_DARK_MODE=true
```

### Using them in React:

```jsx
// Access with import.meta.env
const apiUrl = import.meta.env.VITE_API_URL;
const appName = import.meta.env.VITE_APP_NAME;
const isDarkModeEnabled = import.meta.env.VITE_FEATURE_DARK_MODE === "true";

console.log(import.meta.env.MODE); // "development" or "production"
console.log(import.meta.env.DEV);  // true in development
console.log(import.meta.env.PROD); // true in production
```

---

## 🔑 CRA (Create React App) Environment Variables

In CRA, variables must start with `REACT_APP_`:

```env
# .env (CRA)
REACT_APP_API_URL=https://api.myapp.com
REACT_APP_NAME=My React App
```

```jsx
// Access with process.env
const apiUrl = process.env.REACT_APP_API_URL;
console.log(process.env.NODE_ENV); // "development" or "production"
```

---

## 📁 Multiple .env Files

| File | Used When |
|---|---|
| `.env` | Always (base config) |
| `.env.local` | Local overrides (your machine only) |
| `.env.development` | `npm run dev` (development mode) |
| `.env.production` | `npm run build` (production mode) |
| `.env.test` | Testing environment |

Files are loaded in priority order — `.env.local` overrides `.env`:

```env
# .env (base)
VITE_API_URL=https://api.myapp.com
VITE_DEBUG=false

# .env.development
VITE_API_URL=http://localhost:5000
VITE_DEBUG=true

# .env.production
VITE_API_URL=https://api.myapp.com
VITE_DEBUG=false
```

---

## 🌍 Real-World Usage Example

### services/api.js
```jsx
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,  // Different per environment!
  headers: {
    "Content-Type": "application/json",
    "X-API-Key": import.meta.env.VITE_API_KEY,
  },
});

export default api;
```

### App.jsx
```jsx
function App() {
  const isDev = import.meta.env.DEV;

  return (
    <div>
      {isDev && (
        <div style={{ background: "yellow", padding: "5px" }}>
          ⚠️ Development Mode — API: {import.meta.env.VITE_API_URL}
        </div>
      )}
      <Router />
    </div>
  );
}
```

### Component using env
```jsx
function GoogleMap({ location }) {
  const mapKey = import.meta.env.VITE_GOOGLE_MAPS_KEY;
  const mapUrl = `https://maps.googleapis.com/maps/api/staticmap?center=${location}&key=${mapKey}`;

  return <img src={mapUrl} alt="Map" />;
}
```

---

## 🔒 Security: What's Safe to Put in .env?

| Safe for `.env` | ❌ NOT safe for `.env` |
|---|---|
| Public API baseURL | Database passwords |
| Google Maps public key | JWT secrets |
| Feature flags | Payment gateway secret keys |
| App name/version | Private API keys with billing |

> ⚠️ **WARNING:** Environment variables in Vite/CRA are **embedded in the build** — anyone can see them by inspecting the built JS files! Never put truly secret values like database passwords or private API keys in frontend env files. Those belong on the **backend only**.

---

## 🚫 Always Add `.env` to `.gitignore`

Your `.env.local` and any file with real secrets should **never** be committed to Git:

```gitignore
# .gitignore
.env.local
.env.*.local
```

But the template file is fine to commit:

```env
# .env.example (commit this!)
VITE_API_URL=
VITE_API_KEY=
VITE_GOOGLE_MAPS_KEY=
```

This helps teammates know what env variables are needed without exposing values.

---

## 📋 Hosting Platform Environment Variables

When deploying, set env vars on the hosting platform — not in committed files:

| Platform | Where to set |
|---|---|
| Vercel | Project Settings → Environment Variables |
| Netlify | Site Settings → Build & Deploy → Environment |
| Railway | Project → Variables |
| Heroku | Settings → Config Vars |

---

## ❌ Common Mistakes / Tips

- ❌ Forgetting the `VITE_` prefix (Vite ignores variables without it!)
- ❌ Committing `.env` with real secrets to GitHub
- ❌ Accessing env vars in Node.js style (`process.env`) in Vite — use `import.meta.env`
- ❌ Putting backend secrets in frontend env files
- ✅ Always create a `.env.example` file for teammates
- ✅ Restart the dev server after changing `.env` files!
- 💡 After changing `.env`, stop and restart `npm run dev` — changes don't hot-reload

---

## 📝 Summary

- Env vars let you have **different config per environment** (dev, prod)
- Vite: use `VITE_` prefix, access via `import.meta.env.VITE_*`
- CRA: use `REACT_APP_` prefix, access via `process.env.REACT_APP_*`
- Never commit real secrets — add `.env.local` to `.gitignore`
- Frontend env vars are visible in the browser — don't put truly private data there
- Add `.env.example` for teammates to know what's needed

---

## 🎯 Practice Tasks

1. Create a `.env` file for your Vite app with `VITE_API_URL`
2. Create an axios instance in `services/api.js` that uses `VITE_API_URL`
3. Create a `.env.development` (localhost URL) and `.env.production` (live URL)
4. Add a "Dev Mode" banner that only shows when `import.meta.env.DEV` is true
5. Create a `.env.example` file with all the variable names but empty values

---

> **Previous: [22_folder_structure.md](./22_folder_structure.md)** | **Next: [24_build_deployment.md](./24_build_deployment.md)**
