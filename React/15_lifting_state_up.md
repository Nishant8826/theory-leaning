# 15 - Lifting State Up ⬆️


---

## 🤔 What is Lifting State Up?

When two or more components need to **share the same state**, you move that state up to their **closest common parent** and pass it down as props.

---

## 🧩 The Problem: Sibling Components Need Shared State

```jsx
// ❌ Problem: Two siblings can't access each other's state directly

function TemperatureInput() {
  const [celsius, setCelsius] = useState(0); // Stuck inside here!
  return <input value={celsius} onChange={(e) => setCelsius(e.target.value)} />;
}

function TemperatureDisplay() {
  // ❌ Can't access `celsius` from TemperatureInput — different components!
  return <p>Fahrenheit: ???</p>;
}
```

---

## ✅ The Solution: Lift State to Parent

```jsx
// ✅ Solution: Move state to the parent

function TemperatureConverter() {
  const [celsius, setCelsius] = useState(0); // State lives here

  const fahrenheit = (celsius * 9/5) + 32;

  return (
    <div>
      <TemperatureInput celsius={celsius} onChange={setCelsius} />
      <TemperatureDisplay fahrenheit={fahrenheit} />
    </div>
  );
}

function TemperatureInput({ celsius, onChange }) {
  return (
    <div>
      <label>Celsius: </label>
      <input
        type="number"
        value={celsius}
        onChange={(e) => onChange(Number(e.target.value))}
      />
    </div>
  );
}

function TemperatureDisplay({ fahrenheit }) {
  return <p>🌡️ Fahrenheit: {fahrenheit.toFixed(2)}</p>;
}
```

---

## 🌍 Real-World Examples

### Example 1: Shopping Cart

```jsx
// Parent holds cart state
function ShopPage() {
  const [cart, setCart] = useState([]);

  const addToCart = (item) => {
    setCart([...cart, item]);
  };

  const removeFromCart = (id) => {
    setCart(cart.filter((item) => item.id !== id));
  };

  return (
    <div>
      {/* ProductList can ADD items, Cart can REMOVE items — both share same cart */}
      <ProductList onAddToCart={addToCart} />
      <Cart items={cart} onRemove={removeFromCart} />
    </div>
  );
}

function ProductList({ onAddToCart }) {
  const products = [
    { id: 1, name: "iPhone", price: 79999 },
    { id: 2, name: "AirPods", price: 24900 },
  ];

  return (
    <div>
      <h2>🛍️ Products</h2>
      {products.map((p) => (
        <div key={p.id}>
          <span>{p.name} — ₹{p.price}</span>
          <button onClick={() => onAddToCart(p)}>Add to Cart</button>
        </div>
      ))}
    </div>
  );
}

function Cart({ items, onRemove }) {
  const total = items.reduce((sum, item) => sum + item.price, 0);

  return (
    <div>
      <h2>🛒 Cart ({items.length})</h2>
      {items.map((item, i) => (
        <div key={i}>
          {item.name}
          <button onClick={() => onRemove(item.id)}>❌</button>
        </div>
      ))}
      <p>Total: ₹{total}</p>
    </div>
  );
}
```

### Example 2: Filter + List (Sibling Communication)

```jsx
function App() {
  const [filter, setFilter] = useState("all"); // Lifted up here!

  return (
    <div>
      <FilterBar active={filter} onFilterChange={setFilter} />
      <TaskList filter={filter} />
    </div>
  );
}

function FilterBar({ active, onFilterChange }) {
  return (
    <div>
      {["all", "active", "done"].map((f) => (
        <button
          key={f}
          onClick={() => onFilterChange(f)}
          style={{ fontWeight: active === f ? "bold" : "normal" }}
        >
          {f}
        </button>
      ))}
    </div>
  );
}

function TaskList({ filter }) {
  const tasks = [
    { id: 1, name: "Buy groceries", done: true },
    { id: 2, name: "Go gym", done: false },
    { id: 3, name: "Read book", done: true },
  ];

  const filtered = filter === "all"
    ? tasks
    : tasks.filter((t) => (filter === "done" ? t.done : !t.done));

  return (
    <ul>
      {filtered.map((task) => (
        <li key={task.id}>{task.done ? "✅" : "⬜"} {task.name}</li>
      ))}
    </ul>
  );
}
```

---

## 📐 When to Lift State?

```
Ask yourself: "Which two components need this data?"
         ↓
Find their closest common parent
         ↓
Move the state there
         ↓
Pass down the value (read) and the setter (write) as props
```

---

## 🆚 Lifting State vs Context API

| | Lifting State | Context API |
|---|---|---|
| Best for | 2-3 nearby components | Many components across the app |
| Complexity | Simple | Moderate |
| Prop drilling | Minimal | Eliminated |
| When to use | Local shared state | Global state (theme, auth, language) |

> When prop drilling gets too deep (3+ levels), consider using **Context API** (next topic!)

---

## ❌ Common Mistakes / Tips

- ❌ Keeping state in a child when sibling components also need it
- ❌ Lifting too high — only lift as high as needed
- ✅ State lives in the **lowest common ancestor** of the components that need it
- ✅ Pass both the value AND the updater function as props
- 💡 This pattern is the key to component communication!

---

## 📝 Summary

- Lift state to the **closest common parent** when siblings need to share it
- Parent holds state, children receive it as **props**
- Pass the setter function as a prop so children can **update** the shared state
- For deep hierarchies, consider **Context API** instead

---

## 🎯 Practice Tasks

1. Build a **temperature converter** — type in Celsius and see Fahrenheit update (and vice versa)
2. Build a **search + results** page — `SearchBar` and `ResultList` are siblings. Lift the query state
3. Build a **tab system** — clicking a tab in `TabBar` shows content in `TabContent` (lift active tab)
4. Build a **light switch** — two separate `LightSwitch` components that both control the same light
5. Refactor your Todo app to have `AddTodo` and `TodoList` as separate components that share state via a parent

---

← Previous: [14_lifecycle.md](14_lifecycle.md) | Next: [16_context_api.md](16_context_api.md) →
