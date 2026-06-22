# 03 - JSX (JavaScript XML) 📝

> [!NOTE]
> ### 💡 Topic Quick Overview (For Beginners)
> - **What is it?** JSX (JavaScript XML) is a syntax extension that lets you write HTML structure directly inside your JavaScript code.
> - **Why do we use it?** It makes UI layouts easy to write and read, keeping logic and visual structure together instead of separating them or writing verbose creation functions.
> - **How does it work?** Return JSX tags from components. Wrap JavaScript expressions in curly braces `{}` to render dynamic data, evaluate math, or run logic.

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

## Hinglish Explanation

JSX (JavaScript XML) ka matlab hai JavaScript ke andar HTML-like code likhna.

* **Compilation:** Browser JSX ko direct read nahi kar sakte. Vite ya Babel compile-time par har JSX line ko standard `React.createElement()` call me transform kar dega.
* **Rules:**
  1. Single Parent element return karna zaroori hai. Multiple sibling elements return karne ke liye unhe ek parent wrapper division ya React Fragment `<></>` me wrap karna padta hai.
  2. HTML names vs JSX names: HTML `class` ke badle JSX me `className` aur `for` ke badle `htmlFor` use hota hai.
  3. Expression embedding: Curly braces `{}` ka use karke dynamic variables, function calls aur calculations ko direct HTML elements ke beech show kiya jata hai.

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

### 🔍 Deep Dive: How `React.createElement` Works

If you ever had to write React without JSX, you would use `React.createElement` directly. Here is its syntax:

```javascript
React.createElement(type, props, ...children)
```

#### 🧩 Arguments Breakdown:
1. **`type`**: The HTML tag name as a string (like `"div"`, `"h1"`, or `"button"`), or a custom React component reference.
2. **`props`**: An object containing HTML attributes, classes, and event listeners (like `{ id: "main-title", className: "header" }`). If there are no attributes, pass `null`.
3. **`...children`**: Anything that goes *inside* the element. This can be plain text, other React elements, or JavaScript variables.

#### 🆚 Comparison: JSX vs `React.createElement`

| Desired HTML | Written in JSX | Written using `React.createElement` |
| :--- | :--- | :--- |
| **Simple tag** | `<h1>Hello</h1>` | `React.createElement("h1", null, "Hello")` |
| **Tag with attributes** | `<p id="para">Text</p>` | `React.createElement("p", { id: "para" }, "Text")` |
| **Nested elements** | `<div><span>Hi</span></div>` | `React.createElement("div", null, React.createElement("span", null, "Hi"))` |

As you can see, nesting elements without JSX quickly becomes a nesting nightmare of parentheses, which is why JSX is so widely loved and used! 🚀

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

## 🎤 Interview Questions

> ### ❓ Q1: What is JSX and why do we use it in React?
>
> **Answer:** JSX is a syntax extension for JavaScript that allows you to write HTML-like structures directly inside JS code. We use it because it makes writing React components highly readable and intuitive compared to writing raw `React.createElement` functions.
> * **Hinglish Explanation**: JSX JavaScript ka ek dynamic formatting option hai jo HTML aur JS code ko mix likhne ki permission deta hai. Yeh component layout structure ko clean aur maintainable banata hai.

> ### ❓ Q2: Can web browsers read JSX directly?
>
> **Answer:** No. Browsers can only read standard JavaScript. JSX must be compiled down to standard JavaScript (specifically `React.createElement` calls) using a tool like Babel or Vite before the browser executes it.
> * **Hinglish Explanation**: Nahi, browsers JSX ko direct interpret nahi kar sakte. Transpilers (Babel ya Vite ESBuild) compile status par code ko transform karke `React.createElement` functions me convert karte hain, jise browsers easily execute kar sakte hain.

> ### ❓ Q3: Why must JSX return a single parent element?
>
> **Answer:** Because JSX is translated into functional calls under the hood (`React.createElement()`), a function can only return one single object value at a time. A wrapper `<div />` or a React Fragment `<></>` helps bundle multiple elements into one return value.
> * **Hinglish Explanation**: Under the hood, JSX compiles hokar dynamic function `React.createElement()` call me transform hota hai. Ek time par koi function sirf ek hi single object value return kar sakta hai, isliye hum saare tags ko ek parent block me wrap karte hain.

> ### ❓ Q4: How do you add CSS inline styles in JSX?
>
> **Answer:** You must pass a JavaScript object containing camelCased CSS properties. This requires double curly braces: the first pair tells JSX to evaluate a JavaScript expression, and the second pair represents the actual JavaScript object (e.g. `style={{ color: 'red' }}`).
> * **Hinglish Explanation**: Inline styles ke liye double curly braces `style={{ color: "red" }}` use hote hain. Pehla brace expression evaluation ke liye hota hai aur doosra brace key-value pairs wala style object represent karta hai.

---

← Previous: [02_setup_react.md](02_setup_react.md) | Index: [00_Index.md](00_Index.md) | Next: [04_components.md](04_components.md) →
