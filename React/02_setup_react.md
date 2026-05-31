# 02 - Setting Up React ⚙️

> [!NOTE]
> ### 💡 Topic Quick Overview (For Beginners)
> - **What is it?** React setup involves installing runtime tools (Node.js/npm) and scaffolding a project structure using modern build tools like Vite.
> - **Why do we use it?** Browsers can't read JSX or modern modules directly. Build tools compile and bundle the files into optimized HTML, CSS, and JS that browsers can execute.
> - **How does it work?** Run `npm create vite@latest` to scaffold the app, install dependencies, and start the development server using `npm run dev`.

---

## 🛠️ What You Need First

Before creating a React app, make sure you have these installed:

- **Node.js** — [Download here](https://nodejs.org) (LTS version recommended)
- **npm** or **yarn** — comes with Node.js automatically
- **VS Code** — [Download here](https://code.visualstudio.com/)

### Check if Node is installed:
```bash
node -v    # Should show something like v18.x.x
npm -v     # Should show something like 9.x.x
```

---

## 🚀 Method 1: Vite (⭐ Recommended — Fast & Modern)

> Vite is like a super-fast car. It starts instantly and is the modern way to create React apps.

```bash
# Step 1: Create the app
npm create vite@latest my-app -- --template react

# Step 2: Go into the folder
cd my-app

# Step 3: Install dependencies
npm install

# Step 4: Start the dev server
npm run dev
```

Your app will open at: **http://localhost:5173** 🎉

---

## 🐌 Method 2: Create React App (CRA — Older, Slower)

> CRA is the old way. Still works, but Vite is much faster. Use this only if required.

```bash
# Create the app
npx create-react-app my-app

# Go into the folder
cd my-app

# Start the dev server
npm start
```

Your app opens at: **http://localhost:3000**

---

## 📁 Understanding the Folder Structure (Vite)

```
my-app/
├── public/           ← Static files (images, favicon, etc.)
├── src/              ← YOUR CODE LIVES HERE
│   ├── App.jsx       ← Main component
│   ├── App.css       ← Styles for App
│   ├── main.jsx      ← Entry point (don't touch much)
│   └── index.css     ← Global styles
├── index.html        ← The ONE HTML file React uses
├── package.json      ← Project config and dependencies
└── vite.config.js    ← Vite configuration
```

---

## 📁 Understanding the Folder Structure (CRA)

```
my-app/
├── public/           ← Static files
├── src/
│   ├── App.js        ← Main component
│   ├── App.css
│   ├── index.js      ← Entry point
│   └── index.css
├── package.json
└── ...
```

---

## 🔍 What is `main.jsx` / `index.js`?

This is the **starting point** of your React app. It tells React: *"Hey, put the whole app inside this HTML div!"*

```jsx
// main.jsx (Vite)
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

In `index.html`, there's a div with `id="root"`:
```html
<div id="root"></div>  <!-- React fills this! -->
```

---

## ⚡ Vite vs Create React App

| Feature | Vite | CRA |
|---|---|---|
| Speed | ⚡ Very Fast | 🐢 Slow |
| Modern | ✅ Yes | ❌ Outdated |
| Build Tool | ESBuild + Rollup | Webpack |
| Community | Growing | Declining |
| Recommended | ✅ Yes | ❌ Not anymore |

---

## 🧩 Useful VS Code Extensions for React

Install these from the VS Code extension marketplace:

| Extension | What it does |
|---|---|
| **ES7+ React Snippets** | Type `rafce` → auto-generates component |
| **Prettier** | Auto-formats your code |
| **ESLint** | Catches code errors |
| **Auto Import** | Auto-imports components |

---

## ❌ Common Mistakes / Tips

- ❌ Don't use CRA for new projects — it's slow and outdated
- ✅ Always use `npm create vite@latest` for new projects
- ❌ Don't delete `main.jsx` or `index.html`
- ✅ Your main work happens inside `src/`
- 💡 `npm run dev` = development mode (fast, live reload)
- 💡 `npm run build` = production build (optimized)

---

## 📝 Summary

- Install **Node.js** first
- Use **Vite** to create React apps (`npm create vite@latest`)
- Run `npm install` then `npm run dev` to start
- Your app lives in the `src/` folder
- `main.jsx` is the entry point — connects React to HTML

---

← Previous: [01_introduction.md](01_introduction.md) | Index: [00_Index.md](00_Index.md) | Next: [03_jsx.md](03_jsx.md) →
