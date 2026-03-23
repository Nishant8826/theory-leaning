# 18 - API Calls (fetch / axios) 🌐

> **Previous: [17_react_router.md](./17_react_router.md)** | **Next: [19_error_handling.md](./19_error_handling.md)**

---

## 🤔 What are API Calls?

API calls let your React app **communicate with a backend server** to get or send data.

> **Real-world analogy:**
> Think of a restaurant. You (React app) give your order to the waiter (API). The waiter goes to the kitchen (backend/server), gets your food (data), and brings it back. The API is the waiter!

---

## 🔧 Two Ways to Make API Calls

| | `fetch` (built-in) | `axios` (library) |
|---|---|---|
| Install needed | ❌ No | ✅ `npm install axios` |
| Auto JSON parse | ❌ Need `.json()` | ✅ Done automatically |
| Error handling | Manual | Better (throws on 4xx/5xx) |
| Cancel requests | Complex | Easy with `AbortController` |
| Request config | Verbose | Cleaner |
| Recommended | For simple cases | For production apps |

---

## 📡 Method 1: `fetch` API

### GET Request
```jsx
function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("https://jsonplaceholder.typicode.com/users")
      .then((res) => {
        if (!res.ok) throw new Error("Something went wrong");
        return res.json();         // Must parse JSON manually!
      })
      .then((data) => {
        setUsers(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>⏳ Loading...</p>;
  if (error) return <p>❌ Error: {error}</p>;

  return (
    <ul>
      {users.map((u) => (
        <li key={u.id}>{u.name} — {u.email}</li>
      ))}
    </ul>
  );
}
```

### POST Request with `fetch`
```jsx
const createPost = async () => {
  const response = await fetch("https://jsonplaceholder.typicode.com/posts", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      title: "My Post",
      body: "Post content here",
      userId: 1,
    }),
  });

  const data = await response.json();
  console.log("Created:", data);
};
```

---

## 📡 Method 2: `axios` (Recommended)

### Install
```bash
npm install axios
```

### GET Request
```jsx
import axios from "axios";

function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get("https://jsonplaceholder.typicode.com/users")
      .then((res) => {
        setUsers(res.data); // No need for .json()!
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>⏳ Loading...</p>;
  if (error) return <p>❌ {error}</p>;
  return <ul>{users.map((u) => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

### Using async/await with axios
```jsx
function App() {
  const [posts, setPosts] = useState([]);

  const fetchPosts = async () => {
    try {
      const res = await axios.get("https://jsonplaceholder.typicode.com/posts");
      setPosts(res.data);
    } catch (error) {
      console.error("Failed:", error.message);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  return <ul>{posts.map((p) => <li key={p.id}>{p.title}</li>)}</ul>;
}
```

---

## 🌍 Real-World CRUD Example

```jsx
import axios from "axios";

const API = "https://jsonplaceholder.typicode.com/posts";

function PostManager() {
  const [posts, setPosts] = useState([]);

  // READ
  useEffect(() => {
    axios.get(API).then((res) => setPosts(res.data.slice(0, 5)));
  }, []);

  // CREATE
  const createPost = async () => {
    const newPost = { title: "New Post", body: "Content...", userId: 1 };
    const res = await axios.post(API, newPost);
    setPosts([res.data, ...posts]);
  };

  // UPDATE
  const updatePost = async (id) => {
    const res = await axios.put(`${API}/${id}`, { title: "Updated ✅" });
    setPosts(posts.map((p) => (p.id === id ? res.data : p)));
  };

  // DELETE
  const deletePost = async (id) => {
    await axios.delete(`${API}/${id}`);
    setPosts(posts.filter((p) => p.id !== id));
  };

  return (
    <div>
      <button onClick={createPost}>➕ Add Post</button>
      {posts.map((post) => (
        <div key={post.id} style={{ border: "1px solid #ccc", margin: "8px", padding: "8px" }}>
          <h3>{post.title}</h3>
          <button onClick={() => updatePost(post.id)}>✏️ Update</button>
          <button onClick={() => deletePost(post.id)}>🗑️ Delete</button>
        </div>
      ))}
    </div>
  );
}
```

---

## 🏗️ Axios Instance (Best Practice)

Create a central axios instance so you don't repeat base URL and headers:

```jsx
// api/axiosInstance.js
import axios from "axios";

const api = axios.create({
  baseURL: "https://your-api.com/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Auto-attach JWT token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default api;
```

```jsx
// Usage — clean and reusable!
import api from "./api/axiosInstance";

const res = await api.get("/users");
const res = await api.post("/login", { email, password });
```

---

## ⏳ Loading States Pattern

```jsx
function DataComponent() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await axios.get("/api/data");
      setData(res.data);
    } catch (err) {
      setError(err.response?.data?.message || "Something went wrong");
    } finally {
      setLoading(false); // Always runs!
    }
  };

  if (loading) return <div>⏳ Loading...</div>;
  if (error) return <div>❌ {error}</div>;
  if (!data) return <div>No data yet</div>;

  return <div>{data.title}</div>;
}
```

---

## ❌ Common Mistakes / Tips

- ❌ Making API calls without `useEffect` (runs on every render!)
- ❌ Not handling loading/error states (bad UX)
- ❌ Using `fetch` and forgetting to call `.json()`
- ✅ Always have 3 states: `loading`, `data`, `error`
- ✅ Use `axios` for production — better error handling and cleaner syntax
- ✅ Create a shared `axiosInstance` with base URL and auth headers
- 💡 `try/catch/finally` is cleaner than `.then().catch()` for async/await

---

## 📝 Summary

- Use `fetch` for simple cases, `axios` for real applications
- Always call API inside `useEffect` (with `[]` for on-mount)
- Track 3 states: `loading`, `data`, `error`
- Use `async/await` with `try/catch/finally` for cleaner code
- Create an **axios instance** with base URL and interceptors for large apps

---

## 🎯 Practice Tasks

1. Fetch and display users from `https://jsonplaceholder.typicode.com/users`
2. Fetch posts from `https://jsonplaceholder.typicode.com/posts` with loading + error states
3. Implement a **POST** — add a new post when a form is submitted
4. Build a **search that fetches** results from the API as you type (debounce it!)
5. Create an `axiosInstance` file and use it instead of plain axios

---

> **Previous: [17_react_router.md](./17_react_router.md)** | **Next: [19_error_handling.md](./19_error_handling.md)**
