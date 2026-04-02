# 22 - Folder Structure Best Practices 📁


---

## 🤔 Why Folder Structure Matters?

A good folder structure makes your codebase:
- Easy to navigate
- Easy to scale as the app grows
- Easy for teammates to understand
- Easier to maintain long-term

> **Real-world analogy:**
> A good filing cabinet has labeled drawers (folders) with organized sections. A messy one with everything dumped in one spot wastes hours looking for things. Your `src/` folder is that cabinet!

---

## 🗂️ Small App Structure (< 20 components)

```
src/
├── components/         ← All reusable components
│   ├── Navbar.jsx
│   ├── Footer.jsx
│   └── Button.jsx
├── pages/              ← Full page components (routes)
│   ├── Home.jsx
│   ├── About.jsx
│   └── Contact.jsx
├── App.jsx
├── main.jsx
└── index.css
```

---

## 🏗️ Medium App Structure (Real-World Standard)

```
src/
├── assets/             ← Images, fonts, icons
│   ├── images/
│   └── icons/
│
├── components/         ← Shared/common reusable components
│   ├── Navbar/
│   │   ├── Navbar.jsx
│   │   └── Navbar.css
│   ├── Button/
│   │   └── Button.jsx
│   └── Modal/
│       └── Modal.jsx
│
├── pages/              ← Page-level components (one per route)
│   ├── Home/
│   │   ├── Home.jsx
│   │   └── Home.css
│   ├── Dashboard/
│   │   ├── Dashboard.jsx
│   │   └── components/   ← Page-specific components
│   │       └── StatCard.jsx
│   └── Profile/
│       └── Profile.jsx
│
├── hooks/              ← Custom hooks
│   ├── useFetch.js
│   ├── useAuth.js
│   └── useDebounce.js
│
├── context/            ← Context providers
│   ├── AuthContext.jsx
│   └── ThemeContext.jsx
│
├── services/           ← API calls and external services
│   ├── api.js          ← axios instance
│   ├── userService.js
│   └── postService.js
│
├── utils/              ← Helper functions (pure, no React)
│   ├── formatDate.js
│   ├── formatCurrency.js
│   └── validators.js
│
├── constants/          ← Constant values
│   ├── routes.js
│   └── config.js
│
├── App.jsx
├── main.jsx
└── index.css
```

---

## 🏢 Large App Structure (Feature-Based / Domain-Based)

For large apps, group code by **feature** instead of type:

```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   │   ├── LoginForm.jsx
│   │   │   └── RegisterForm.jsx
│   │   ├── hooks/
│   │   │   └── useAuth.js
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   ├── services/
│   │   │   └── authService.js
│   │   └── pages/
│   │       ├── LoginPage.jsx
│   │       └── RegisterPage.jsx
│   │
│   ├── products/
│   │   ├── components/
│   │   │   ├── ProductCard.jsx
│   │   │   └── ProductList.jsx
│   │   ├── hooks/
│   │   │   └── useProducts.js
│   │   ├── services/
│   │   │   └── productService.js
│   │   └── pages/
│   │       ├── ProductsPage.jsx
│   │       └── ProductDetailPage.jsx
│   │
│   └── cart/
│       ├── components/
│       │   └── CartItem.jsx
│       ├── context/
│       │   └── CartContext.jsx
│       └── pages/
│           └── CartPage.jsx
│
├── shared/                 ← Used across multiple features
│   ├── components/
│   │   ├── Button.jsx
│   │   ├── Modal.jsx
│   │   └── Spinner.jsx
│   ├── hooks/
│   │   └── useDebounce.js
│   └── utils/
│       └── formatDate.js
│
├── App.jsx
└── main.jsx
```

---

## 📋 Naming Conventions

| Type | Convention | Example |
|---|---|---|
| Components | PascalCase | `UserCard.jsx`, `Navbar.jsx` |
| Hooks | camelCase with `use` prefix | `useAuth.js`, `useFetch.js` |
| Utilities | camelCase | `formatDate.js`, `validators.js` |
| Context | PascalCase + Context | `AuthContext.jsx`, `ThemeContext.jsx` |
| Services | camelCase + Service | `userService.js`, `authService.js` |
| Constants | UPPER_CASE or camelCase | `API_URL`, `routes.js` |
| CSS Modules | Same as component | `Navbar.module.css` |

---

## 🔗 Services Layer (API Organization)

```jsx
// services/api.js — Central axios instance
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: { "Content-Type": "application/json" },
});

export default api;

// services/userService.js — All user-related API calls
import api from "./api";

export const getUsers = () => api.get("/users");
export const getUserById = (id) => api.get(`/users/${id}`);
export const createUser = (data) => api.post("/users", data);
export const updateUser = (id, data) => api.put(`/users/${id}`, data);
export const deleteUser = (id) => api.delete(`/users/${id}`);
```

```jsx
// Usage in component — clean!
import { getUsers, deleteUser } from "../services/userService";

function UserList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    getUsers().then((res) => setUsers(res.data));
  }, []);
}
```

---

## 📐 Constants File

```jsx
// constants/routes.js
export const ROUTES = {
  HOME: "/",
  LOGIN: "/login",
  DASHBOARD: "/dashboard",
  PROFILE: "/profile/:id",
};

// Usage
import { ROUTES } from "../constants/routes";
<Link to={ROUTES.DASHBOARD}>Dashboard</Link>
```

---

## ✅ Best Practices Checklist

- ✅ One component per file
- ✅ PascalCase for component file names
- ✅ Group by feature in large apps
- ✅ Keep components small and focused (< 200 lines ideally)
- ✅ Create a `services/` layer for all API calls
- ✅ Don't put logic inside JSX — extract to functions/hooks
- ✅ Add an `index.js` to folders for clean imports:
  ```jsx
  // components/index.js
  export { default as Button } from "./Button/Button";
  export { default as Modal } from "./Modal/Modal";
  
  // Usage: clean!
  import { Button, Modal } from "../components";
  ```

---

## ❌ Common Mistakes / Tips

- ❌ Putting all files flat in `src/` — impossible to navigate as app grows
- ❌ Naming component files in lowercase (`navbar.jsx` → ❌, `Navbar.jsx` → ✅)
- ❌ Giant components (1000+ lines) — split into smaller ones!
- ❌ API calls scattered randomly in components — use a `services/` layer
- ✅ Structure should reflect how you think about the app, not just file types

---

## 📝 Summary

- Small apps: `components/`, `pages/` — keep it simple
- Medium apps: Add `hooks/`, `context/`, `services/`, `utils/`
- Large apps: Feature-based structure groups everything by domain
- Always use consistent naming conventions
- Services layer keeps API calls organized and reusable

---

## 🎯 Practice Tasks

1. Take your current project and organize it into `components/`, `pages/`, `hooks/`, `services/`
2. Create a `services/userService.js` with functions for all user API operations
3. Create an `index.js` in `components/` folder for clean barrel exports
4. Create a `constants/routes.js` file and update all your route paths to use it
5. Convert a "flat" folder structure into a feature-based structure for a small app

---

← Previous: [21_performance_optimization.md](21_performance_optimization.md) | Next: [23_environment_variables.md](23_environment_variables.md) →
