# 09 - Lists and Keys 📋


---

## 🤔 What are Lists in React?

A "list" in React means **displaying an array of data** as multiple UI elements.

> **Real-world analogy:**
> Think of a shopping cart on Amazon. You have 5 items in your cart — each item displayed the same way (image, name, price, quantity). React renders all of them by **looping** over the data array.

---

## 🔄 Rendering Lists with `.map()`

The most common way to render a list in React is using the `.map()` array method:

```tsx
function FruitList() {
  const fruits = ["🍎 Apple", "🍌 Banana", "🍊 Orange", "🍇 Grapes"];

  return (
    <ul>
      {fruits.map((fruit, index) => (
        <li key={index}>{fruit}</li>
      ))}
    </ul>
  );
}
```

---

## 🔑 What is a `key`?

A `key` is a **unique identifier** you give to each item in a list. React uses it to:
- Track which items changed, were added, or removed
- Efficiently update only the necessary DOM elements

> **Analogy:** Imagine 100 students with roll numbers. If a student leaves, instead of checking all 100 names, you just delete roll number 47. Keys work the same way for React!

---

## ✅ Good Keys vs ❌ Bad Keys

```tsx
// ❌ BAD: Using array index as key (causes bugs when order changes)
{items.map((item, index) => <li key={index}>{item}</li>)}

// ✅ GOOD: Using a unique ID from the data
{items.map((item) => <li key={item.id}>{item.name}</li>)}
```

> 💡 Only use `index` as key when:
> - The list never changes order
> - Items are never added/removed
> - It's a static simple list

---

## 🌍 Real-World Examples

### Example 1: Product List (From Array of Objects)

```tsx
const products = [
  { id: 1, name: "iPhone 15", price: "₹79,999", qty: 5 },
  { id: 2, name: "MacBook Air", price: "₹1,14,900", qty: 3 },
  { id: 3, name: "AirPods Pro", price: "₹24,900", qty: 10 },
];

function ProductList() {
  return (
    <div>
      <h2>🛍️ Products</h2>
      {products.map((product) => (
        <div key={product.id} className="product-card">
          <h3>{product.name}</h3>
          <p>Price: {product.price}</p>
          <p>In Stock: {product.qty}</p>
        </div>
      ))}
    </div>
  );
}
```

### Example 2: Dynamic Todo List

```tsx
function TodoList() {
  const [todos, setTodos] = useState([
    { id: 1, text: "Buy groceries", done: false },
    { id: 2, text: "Go for a run", done: true },
    { id: 3, text: "Read a book", done: false },
  ]);

  const toggleTodo = (id) => {
    setTodos(todos.map((todo) =>
      todo.id === id ? { ...todo, done: !todo.done } : todo
    ));
  };

  return (
    <ul>
      {todos.map((todo) => (
        <li
          key={todo.id}
          style={{ textDecoration: todo.done ? "line-through" : "none" }}
          onClick={() => toggleTodo(todo.id)}
        >
          {todo.done ? "✅" : "⬜"} {todo.text}
        </li>
      ))}
    </ul>
  );
}
```

### Example 3: Table from API-like Data

```tsx
const users = [
  { id: 101, name: "Nishant", email: "nishant@dev.com", role: "Admin" },
  { id: 102, name: "Priya", email: "priya@dev.com", role: "User" },
  { id: 103, name: "Raj", email: "raj@dev.com", role: "Editor" },
];

function UserTable() {
  return (
    <table border="1">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Role</th>
        </tr>
      </thead>
      <tbody>
        {users.map((user) => (
          <tr key={user.id}>
            <td>{user.id}</td>
            <td>{user.name}</td>
            <td>{user.email}</td>
            <td>{user.role}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

---

## 🔗 Nested Lists

```tsx
const categories = [
  {
    id: 1,
    name: "Frontend",
    skills: ["React", "CSS", "JavaScript"],
  },
  {
    id: 2,
    name: "Backend",
    skills: ["Node.js", "Express", "MongoDB"],
  },
];

function SkillTree() {
  return (
    <div>
      {categories.map((cat) => (
        <div key={cat.id}>
          <h3>{cat.name}</h3>
          <ul>
            {cat.skills.map((skill, i) => (
              <li key={i}>{skill}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
```

---

## 🔍 Filtering Lists

```tsx
function FilteredList() {
  const [filter, setFilter] = useState("all");

  const items = [
    { id: 1, name: "React", type: "frontend" },
    { id: 2, name: "Node.js", type: "backend" },
    { id: 3, name: "CSS", type: "frontend" },
    { id: 4, name: "MongoDB", type: "backend" },
  ];

  const filtered = filter === "all"
    ? items
    : items.filter((item) => item.type === filter);

  return (
    <div>
      <button onClick={() => setFilter("all")}>All</button>
      <button onClick={() => setFilter("frontend")}>Frontend</button>
      <button onClick={() => setFilter("backend")}>Backend</button>

      <ul>
        {filtered.map((item) => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

---

## ❌ Common Mistakes / Tips

- ❌ Forgetting the `key` prop (React warns you + performance suffers)
- ❌ Using non-unique keys (two items same key = bugs!)
- ❌ Using array index for dynamic lists where order can change
- ✅ Always use a **unique ID** (from database or generated) as key
- ✅ Key goes on the outermost element of the `.map()` return
- 💡 Keys must only be unique among **siblings**, not globally

---

## 📝 Summary

- Use `.map()` to render lists in React
- Always add a `key` prop to each list item
- Use **unique IDs** as keys, not array indexes (unless list is static)
- Keys help React efficiently update the UI
- Use `.filter()` + `.map()` for filtered lists

---

## 🎯 Practice Tasks

1. Render a list of 5 countries with their capitals using `.map()`
2. Render an array of students in a table (name, age, grade)
3. Build a **filterable list** — filter by category (e.g., fruits, vegetables)
4. Build a **searchable list** — type to filter items in real-time
5. Build a list where you can click to remove an item (use `.filter()`)

---

← Previous: [08_conditional_rendering.md](08_conditional_rendering.md) | Next: [10_forms.md](10_forms.md) →
