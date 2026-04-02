# 27 - Mini Project Guide 🏗️


---

## 🎯 Overview

This final chapter brings **everything together** with two mini project guides:
1. **Todo App** — Perfect beginner project (covers state, events, forms, lists)
2. **Blog App** — Intermediate project (covers API, routing, context, components)

Complete at least one of these to solidify your React learning!

---

# 📌 Project 1: Todo App ✅

## What You'll Practice
- `useState` for state management
- Event handling (click, submit)
- Conditional rendering
- Lists and keys
- Forms (controlled inputs)
- Component composition

## 🎨 Features to Build
- [ ] Add new todos
- [ ] Mark as complete / incomplete (with strikethrough)
- [ ] Delete a todo
- [ ] Filter todos (All / Active / Completed)
- [ ] Show count of remaining tasks
- [ ] Persist todos to `localStorage`

---

## 🗂️ Project Structure

```
todo-app/
├── src/
│   ├── components/
│   │   ├── TodoInput.jsx      ← Input form
│   │   ├── TodoList.jsx       ← List of todos
│   │   ├── TodoItem.jsx       ← Single todo
│   │   └── FilterBar.jsx      ← Filter buttons
│   ├── hooks/
│   │   └── useTodos.js        ← Custom hook for todo logic
│   ├── App.jsx
│   └── index.css
```

---

## 📄 Step-by-Step Code

### Step 1: `useTodos.js` — Custom Hook for All Logic

```jsx
// hooks/useTodos.js
import { useState, useEffect } from "react";

const STORAGE_KEY = "react-todos";

function useTodos() {
  const [todos, setTodos] = useState(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved ? JSON.parse(saved) : [];
  });

  const [filter, setFilter] = useState("all"); // "all" | "active" | "completed"

  // Save to localStorage whenever todos change
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
  }, [todos]);

  const addTodo = (text) => {
    if (!text.trim()) return;
    setTodos([...todos, { id: Date.now(), text, completed: false }]);
  };

  const toggleTodo = (id) => {
    setTodos(todos.map((t) => (t.id === id ? { ...t, completed: !t.completed } : t)));
  };

  const deleteTodo = (id) => {
    setTodos(todos.filter((t) => t.id !== id));
  };

  const clearCompleted = () => {
    setTodos(todos.filter((t) => !t.completed));
  };

  const filteredTodos = todos.filter((t) => {
    if (filter === "active") return !t.completed;
    if (filter === "completed") return t.completed;
    return true;
  });

  const remaining = todos.filter((t) => !t.completed).length;

  return { filteredTodos, filter, setFilter, addTodo, toggleTodo, deleteTodo, clearCompleted, remaining };
}

export default useTodos;
```

### Step 2: `TodoInput.jsx`

```jsx
// components/TodoInput.jsx
import { useState } from "react";

function TodoInput({ onAdd }) {
  const [text, setText] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onAdd(text);
    setText("");
  };

  return (
    <form onSubmit={handleSubmit} className="todo-input-form">
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="What needs to be done? ✍️"
        className="todo-input"
      />
      <button type="submit" className="todo-add-btn">Add</button>
    </form>
  );
}

export default TodoInput;
```

### Step 3: `TodoItem.jsx`

```jsx
// components/TodoItem.jsx
function TodoItem({ todo, onToggle, onDelete }) {
  return (
    <li className={`todo-item ${todo.completed ? "completed" : ""}`}>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo.id)}
      />
      <span
        style={{ textDecoration: todo.completed ? "line-through" : "none" }}
      >
        {todo.text}
      </span>
      <button onClick={() => onDelete(todo.id)} className="delete-btn">
        🗑️
      </button>
    </li>
  );
}

export default TodoItem;
```

### Step 4: `TodoList.jsx`

```jsx
// components/TodoList.jsx
import TodoItem from "./TodoItem";

function TodoList({ todos, onToggle, onDelete }) {
  if (todos.length === 0) {
    return <p className="empty-state">No todos! 🎉 You're all caught up.</p>;
  }

  return (
    <ul className="todo-list">
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={onToggle}
          onDelete={onDelete}
        />
      ))}
    </ul>
  );
}

export default TodoList;
```

### Step 5: `FilterBar.jsx`

```jsx
// components/FilterBar.jsx
function FilterBar({ filter, onFilter, remaining, onClearCompleted }) {
  return (
    <div className="filter-bar">
      <span>{remaining} items left</span>

      <div className="filter-buttons">
        {["all", "active", "completed"].map((f) => (
          <button
            key={f}
            onClick={() => onFilter(f)}
            className={filter === f ? "active" : ""}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      <button onClick={onClearCompleted}>Clear Completed</button>
    </div>
  );
}

export default FilterBar;
```

### Step 6: `App.jsx` — Assemble

```jsx
// App.jsx
import useTodos from "./hooks/useTodos";
import TodoInput from "./components/TodoInput";
import TodoList from "./components/TodoList";
import FilterBar from "./components/FilterBar";
import "./index.css";

function App() {
  const { filteredTodos, filter, setFilter, addTodo, toggleTodo, deleteTodo, clearCompleted, remaining } = useTodos();

  return (
    <div className="app">
      <h1>📝 My Todo App</h1>
      <div className="todo-container">
        <TodoInput onAdd={addTodo} />
        <TodoList todos={filteredTodos} onToggle={toggleTodo} onDelete={deleteTodo} />
        <FilterBar
          filter={filter}
          onFilter={setFilter}
          remaining={remaining}
          onClearCompleted={clearCompleted}
        />
      </div>
    </div>
  );
}

export default App;
```

---

# 📌 Project 2: Blog App 📰

## What You'll Practice
- API calls (fetch / axios)
- React Router (navigation)
- Context API (theme)
- Custom hooks
- useEffect
- Loading / error states

## 🎨 Features to Build
- [ ] Home page with list of blog posts (from API)
- [ ] Click a post → View full post detail
- [ ] Search posts by title
- [ ] Loading and error states
- [ ] Dark/light mode toggle (Context)
- [ ] Navigate between pages (React Router)

---

## 🗂️ Project Structure

```
blog-app/
├── src/
│   ├── pages/
│   │   ├── Home.jsx          ← List of posts
│   │   └── PostDetail.jsx    ← Single post view
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── PostCard.jsx
│   │   └── SearchBar.jsx
│   ├── hooks/
│   │   └── usePosts.js
│   ├── context/
│   │   └── ThemeContext.jsx
│   ├── services/
│   │   └── api.js
│   ├── App.jsx
│   └── main.jsx
```

---

## 📄 Key Code Pieces

### `services/api.js`
```jsx
import axios from "axios";
const api = axios.create({ baseURL: "https://jsonplaceholder.typicode.com" });
export const getPosts = () => api.get("/posts");
export const getPost = (id) => api.get(`/posts/${id}`);
export const getComments = (postId) => api.get(`/posts/${postId}/comments`);
export default api;
```

### `hooks/usePosts.js`
```jsx
import { useState, useEffect } from "react";
import { getPosts } from "../services/api";

function usePosts(search = "") {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    getPosts()
      .then((res) => setPosts(res.data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const filtered = posts.filter((p) =>
    p.title.toLowerCase().includes(search.toLowerCase())
  );

  return { posts: filtered, loading, error };
}

export default usePosts;
```

### `pages/Home.jsx`
```jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import usePosts from "../hooks/usePosts";
import PostCard from "../components/PostCard";
import SearchBar from "../components/SearchBar";

function Home() {
  const [search, setSearch] = useState("");
  const { posts, loading, error } = usePosts(search);
  const navigate = useNavigate();

  if (loading) return <p>⏳ Loading posts...</p>;
  if (error) return <p>❌ Error: {error}</p>;

  return (
    <div className="home">
      <h1>📰 React Blog</h1>
      <SearchBar value={search} onChange={setSearch} />
      <div className="post-grid">
        {posts.slice(0, 12).map((post) => (
          <PostCard
            key={post.id}
            post={post}
            onClick={() => navigate(`/posts/${post.id}`)}
          />
        ))}
      </div>
    </div>
  );
}

export default Home;
```

### `pages/PostDetail.jsx`
```jsx
import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { getPost, getComments } from "../services/api";

function PostDetail() {
  const { id } = useParams();
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getPost(id), getComments(id)])
      .then(([postRes, commentsRes]) => {
        setPost(postRes.data);
        setComments(commentsRes.data);
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <p>⏳ Loading...</p>;
  if (!post) return <p>Post not found</p>;

  return (
    <div className="post-detail">
      <Link to="/">← Back to posts</Link>
      <h1>{post.title}</h1>
      <p>{post.body}</p>

      <h2>💬 Comments ({comments.length})</h2>
      {comments.map((c) => (
        <div key={c.id} className="comment">
          <strong>{c.email}</strong>
          <p>{c.body}</p>
        </div>
      ))}
    </div>
  );
}

export default PostDetail;
```

---

## 🎯 Bonus Challenges (Push Further!)

### For Todo App:
- Add **drag and drop** to reorder todos
- Add **due dates** with a date picker
- Add **categories/labels** to todos
- Add **animations** when adding/removing todos

### For Blog App:
- Add a **favorites** feature using Context
- Add **pagination** (show 10 posts per page)
- Add a **Create Post** page with a form
- Add **user profile** pages

---

## 📝 Final Summary: What You've Learned

By completing these projects you've applied:

| Topic | Used In |
|---|---|
| Components | Both projects |
| Props | Both projects |
| State (`useState`) | Todo App |
| Events | Both projects |
| Forms | Todo App |
| `useEffect` | Blog App |
| API calls | Blog App |
| React Router | Blog App |
| Context API | Blog App (theme) |
| Custom Hooks | Both projects |
| Lists & Keys | Both projects |
| Conditional Rendering | Both projects |
| Error Handling | Blog App |
| localStorage | Todo App |

**You're now ready to build real React apps! 🎉**

---

## 🚀 Next Steps After This

1. **Build your own project** — a portfolio site, a recipe app, a quiz app
2. **Learn Next.js** — React with SSR, routing, and full-stack features
3. **Learn Redux Toolkit** — for complex global state management
4. **Learn React Query / TanStack Query** — for powerful data fetching
5. **Contribute to open source** — real experience!
6. **Build and deploy** — get your project live on Vercel/Netlify
7. **Start applying for jobs** — React is one of the most in-demand skills!

---

## 🏆 Congratulations!

You've completed the **React Learning Handbook**! 🎉

Going from 0 to knowing React is a huge achievement. Keep building, keep learning, and don't be afraid to make mistakes — that's how the best developers grow.

**Happy coding! 🚀**

---

>
> 📂 **[View Full Index → README.md](./README.md)**

---

← Previous: [26_best_practices.md](26_best_practices.md) | Next: [README.md](README.md) →
