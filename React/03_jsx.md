# 03 - JSX (JavaScript XML) 📝


---

## 🤔 What is JSX?

JSX stands for **JavaScript XML**. It lets you write **HTML-like code inside JavaScript**.

Think of it like this:

> Normally in a restaurant, the kitchen (JavaScript) and the menu display (HTML) are separate. JSX is like a chef who can write the menu directly **while cooking** — combining both in one place!

```tsx
// This is JSX — looks like HTML but it's inside JavaScript!
const element = <h1>Hello, World!</h1>;
```

---

## 🆚 JSX vs Regular HTML

| Feature | HTML | JSX |
|---|---|---|
| Class | `class="box"` | `className="box"` |
| For | `for="name"` | `htmlFor="name"` |
| Self-close | `<br>` | `<br />` |
| Style | `style="color:red"` | `style={{ color: "red" }}` |
| JS inside | ❌ Can't | ✅ Use `{}` |
| Comments | `<!-- comment -->` | `{/* comment */}` |

---

## 🔧 JSX Rules You MUST Know

### Rule 1: Every JSX must return ONE parent element

```tsx
// ❌ WRONG - two sibling elements at top level
return (
  <h1>Hello</h1>
  <p>World</p>
);

// ✅ CORRECT - wrapped in one parent
return (
  <div>
    <h1>Hello</h1>
    <p>World</p>
  </div>
);

// ✅ ALSO CORRECT - use Fragment (no extra div!)
return (
  <>
    <h1>Hello</h1>
    <p>World</p>
  </>
);
```

### Rule 2: Use `className` instead of `class`

```tsx
// ❌ WRONG
<div class="container">Hello</div>

// ✅ CORRECT
<div className="container">Hello</div>
```

### Rule 3: Self-close all empty tags

```tsx
// ❌ WRONG
<input type="text">
<img src="photo.jpg">

// ✅ CORRECT
<input type="text" />
<img src="photo.jpg" />
```

### Rule 4: Use `{}` to write JavaScript inside JSX

```tsx
const name = "Nishant";
const age = 25;

return (
  <div>
    <p>Hello, {name}!</p>           {/* Variable */}
    <p>Age: {age + 1}</p>           {/* Expression */}
    <p>Today: {new Date().toDateString()}</p>  {/* Function call */}
  </div>
);
```

### Rule 5: Inline styles use double curly braces `{{}}`

```tsx
// ❌ WRONG
<p style="color: red; font-size: 18px">Hello</p>

// ✅ CORRECT - style is an object!
<p style={{ color: "red", fontSize: "18px" }}>Hello</p>
```

> 💡 CSS properties in JSX use **camelCase**: `font-size` → `fontSize`, `background-color` → `backgroundColor`

---

## 🌍 Real-World JSX Examples

### Example 1: Displaying User Info

```tsx
function UserCard() {
  const user = {
    name: "Nishant",
    role: "Developer",
    isActive: true,
  };

  return (
    <div className="user-card">
      <h2>{user.name}</h2>
      <p>Role: {user.role}</p>
      <p>Status: {user.isActive ? "🟢 Active" : "🔴 Inactive"}</p>
    </div>
  );
}
```

### Example 2: Dynamic List

```tsx
function FruitList() {
  const fruits = ["🍎 Apple", "🍌 Banana", "🍊 Orange"];

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

## 🔄 How JSX Works Behind the Scenes

JSX is not real HTML. It gets **compiled** (transformed) into regular JavaScript by **Babel** or **Vite**.

```tsx
// What you write (JSX):
const element = <h1 className="title">Hello</h1>;

// What React actually runs (after compilation):
const element = React.createElement("h1", { className: "title" }, "Hello");
```

You never have to write `React.createElement()` yourself — JSX handles it! 😊

---

## ❌ Common Mistakes / Tips

- ❌ Using `class` instead of `className`
- ❌ Forgetting to self-close tags like `<input>` → must be `<input />`
- ❌ Putting statements (like `if`, `for`) directly in JSX — only **expressions** work
- ✅ Use ternary operator `condition ? "yes" : "no"` instead of `if` inside JSX
- ✅ Use `.map()` instead of `for` loops inside JSX
- 💡 JSX comments: `{/* This is a comment */}`

---

## 📝 Summary

- JSX = **HTML-like syntax inside JavaScript**
- Always return **one parent element** (or use `<>...</>` fragments)
- Use `className` not `class`
- Insert JavaScript with `{}`
- Use double `{{}}` for inline styles
- JSX compiles to `React.createElement()` behind the scenes

---

## 🎯 Practice Tasks

1. Create a `ProfileCard` component that shows: name, age, city — using variables and JSX
2. Create a list of 5 of your favorite movies using `.map()` in JSX
3. Try using a ternary operator to show "Good Morning 🌅" or "Good Night 🌙" based on a variable
4. Apply inline styles to a JSX element using the double `{{}}` syntax
5. Try using a Fragment `<>...</>` and see that no extra `<div>` appears in the browser's DevTools

---

← Previous: [02_setup_react.md](02_setup_react.md) | Next: [04_components.md](04_components.md) →
