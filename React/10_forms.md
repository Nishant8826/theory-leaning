# 10 - Forms and Controlled Components 📝


---

## 🤔 What are Controlled Components?

In React, a **controlled component** is an input element whose value is controlled by **React state**.

> **Real-world analogy:**
> Think of a puppet show. In an uncontrolled form, the puppet moves on its own. In a controlled form, YOU control every move of the puppet (the input) with strings (React state).

```
Typing in input → onChange fires → setState updates → React re-renders → Input shows new value
```

---

## 🆚 Controlled vs Uncontrolled Components

| Feature | Controlled | Uncontrolled |
|---|---|---|
| Value stored in | React state | DOM itself |
| Access value via | `state` variable | `ref.current.value` |
| React controls? | ✅ Yes | ❌ No |
| Real-time validation | ✅ Easy | ❌ Hard |
| Recommended? | ✅ Yes | For simple cases |

---

## 🔧 Basic Controlled Input

```tsx
function ControlledInput() {
  const [value, setValue] = useState("");

  return (
    <div>
      <input
        type="text"
        value={value}               {/* Controlled by state */}
        onChange={(e) => setValue(e.target.value)}  {/* Updates state */}
        placeholder="Type here..."
      />
      <p>You typed: <strong>{value}</strong></p>
    </div>
  );
}
```

---

## 🌍 Real-World Form Example: Registration Form

```tsx
function RegistrationForm() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    gender: "male",
    terms: false,
  });

  const [errors, setErrors] = useState({});

  // Handle all inputs with ONE function!
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.name) newErrors.name = "Name is required";
    if (!formData.email.includes("@")) newErrors.email = "Invalid email";
    if (formData.password.length < 6) newErrors.password = "Min 6 characters";
    if (!formData.terms) newErrors.terms = "You must accept terms";
    return newErrors;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const newErrors = validate();

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
    } else {
      console.log("Form submitted:", formData);
      alert("Registration successful! 🎉");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Name */}
      <div>
        <label>Name:</label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          placeholder="Your full name"
        />
        {errors.name && <span style={{ color: "red" }}>{errors.name}</span>}
      </div>

      {/* Email */}
      <div>
        <label>Email:</label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="email@example.com"
        />
        {errors.email && <span style={{ color: "red" }}>{errors.email}</span>}
      </div>

      {/* Password */}
      <div>
        <label>Password:</label>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          placeholder="Min 6 characters"
        />
        {errors.password && <span style={{ color: "red" }}>{errors.password}</span>}
      </div>

      {/* Gender (Radio) */}
      <div>
        <label>Gender:</label>
        <label>
          <input type="radio" name="gender" value="male" checked={formData.gender === "male"} onChange={handleChange} />
          Male
        </label>
        <label>
          <input type="radio" name="gender" value="female" checked={formData.gender === "female"} onChange={handleChange} />
          Female
        </label>
      </div>

      {/* Select */}
      <div>
        <label>Country:</label>
        <select name="country" onChange={handleChange}>
          <option value="india">India 🇮🇳</option>
          <option value="usa">USA 🇺🇸</option>
          <option value="uk">UK 🇬🇧</option>
        </select>
      </div>

      {/* Checkbox */}
      <div>
        <label>
          <input
            type="checkbox"
            name="terms"
            checked={formData.terms}
            onChange={handleChange}
          />
          I accept the Terms & Conditions
        </label>
        {errors.terms && <span style={{ color: "red" }}>{errors.terms}</span>}
      </div>

      <button type="submit">Register</button>
    </form>
  );
}
```

---

## 📋 Form Element Cheat Sheet

| Element | `value` binding | `onChange` |
|---|---|---|
| `<input type="text">` | `value={state}` | `e.target.value` |
| `<input type="checkbox">` | `checked={state}` | `e.target.checked` |
| `<input type="radio">` | `checked={state === "value"}` | `e.target.value` |
| `<textarea>` | `value={state}` | `e.target.value` |
| `<select>` | `value={state}` | `e.target.value` |

---

## 📐 Textarea

```tsx
function CommentBox() {
  const [comment, setComment] = useState("");

  return (
    <div>
      <textarea
        value={comment}
        onChange={(e) => setComment(e.target.value)}
        rows={5}
        placeholder="Write your comment..."
      />
      <p>Characters: {comment.length}/200</p>
    </div>
  );
}
```

---

## ❌ Common Mistakes / Tips

- ❌ Forgetting `e.preventDefault()` on form `onSubmit` (causes page reload!)
- ❌ Using `onChange` on the form instead of each input
- ❌ Not using `checked` for checkboxes/radio buttons (use `checked`, not `value`)
- ✅ One `handleChange` function can handle all inputs using `e.target.name`
- ✅ Always validate before submitting
- 💡 `[name]: value` is computed property syntax — super useful for dynamic object updates

---

## 📝 Summary

- Controlled components = form inputs **tied to React state**
- Use `value` + `onChange` to control text inputs, textareas, selects
- Use `checked` + `onChange` for checkboxes and radio buttons
- Always call `e.preventDefault()` in `onSubmit` to prevent page reload
- One `handleChange` function with `e.target.name` can handle all fields

---

## 🎯 Practice Tasks

1. Build a **login form** (email + password) with basic validation
2. Build a **contact form** (name, email, message textarea, submit)
3. Add real-time validation (password must be 8+ chars, email must have @)
4. Build a **survey form** with radio buttons and a dropdown
5. After submit, show a "Thank you!" message and clear the form

---

← Previous: [09_lists_and_keys.md](09_lists_and_keys.md) | Next: [11_useEffect.md](11_useEffect.md) →
