# 03 - JSX (JavaScript XML) 📝


---

## 🤔 What is JSX?

JSX stands for **JavaScript XML**. It lets you write **HTML-like code inside JavaScript**.

```jsx
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

```jsx
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

```jsx
// ❌ WRONG
<div class="container">Hello</div>

// ✅ CORRECT
<div className="container">Hello</div>
```

### Rule 3: Self-close all empty tags

```jsx
// ❌ WRONG
<input type="text">
<img src="photo.jpg">

// ✅ CORRECT
<input type="text" />
<img src="photo.jpg" />
```

### Rule 4: Use `{}` to write JavaScript inside JSX

```jsx
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

```jsx
// ❌ WRONG
<p style="color: red; font-size: 18px">Hello</p>

// ✅ CORRECT - style is an object!
<p style={{ color: "red", fontSize: "18px" }}>Hello</p>
```

> 💡 CSS properties in JSX use **camelCase**: `font-size` → `fontSize`, `background-color` → `backgroundColor`

---

## 🌍 Real-World JSX Examples

### Example 1: Displaying User Info

```jsx
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

- **What:** Writing conditional variables and dynamic data inside a component.
- **Why:** Standard HTML is static; JSX allows embedding JavaScript logic seamlessly to create data-driven structures.
- **How:** We use `{}` interpolation to access `user` object properties and a ternary operator for the conditional `isActive` rendering.
- **Impact:** Enables clean rendering of rich, dynamic components without complex DOM manipulation.

### Example 2: Dynamic List

```jsx
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

- **What:** Looping through an array to generate a list of JSX elements.
- **Why:** To efficiently render data lists without manually copying and pasting repetitive markup.
- **How:** We use the array `.map()` function inside `{}` to iterate over the `fruits` and return an `<li>` for each.
- **Impact:** Drastically reduces code duplication and dynamically handles lists of any size.

---

## 🔄 How JSX Works Behind the Scenes

JSX is not real HTML. It gets **compiled** (transformed) into regular JavaScript by **Babel** or **Vite**.

```jsx
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

## 🎤 Interview Questions

**Q1: What is JSX and why do we use it in React?**
**Answer:** JSX is a syntax extension for JavaScript that allows you to write HTML-like structures directly inside JS code. We use it because it makes writing React components highly readable and intuitive compared to writing raw `React.createElement()` functions.

**Q2: Can web browsers read JSX directly?**
**Answer:** No. Browsers can only read standard JavaScript. JSX must be compiled down to standard JavaScript (specifically `React.createElement` calls) using a tool like Babel or Vite before the browser executes it.

**Q3: Why must JSX return a single parent element?**
**Answer:** Because JSX is translated into functional calls under the hood (`React.createElement()`), a function can only return one single object value at a time. A wrapper `<div />` or a React Fragment `<></>` helps bundle multiple elements into one return value.

**Q4: How do you add CSS inline styles in JSX?**
**Answer:** You must pass a JavaScript object containing camelCased CSS properties. This requires double curly braces: the first pair tells JSX to evaluate a JavaScript expression, and the second pair represents the actual JavaScript object (e.g. `style={{ color: 'red' }}`).

---

← Previous: [02_setup_react.md](02_setup_react.md) | Next: [04_components.md](04_components.md) →
