# 📌 02 — Tricky JavaScript Questions

## 🌟 Introduction

Interviewers love "Tricky" questions because they reveal if you truly understand the language or if you've just memorized patterns.

This file covers the most common **"Gotchas"** and why they happen.

---

## 🏗️ 1. The Loop & `var` Trap

**Q: What is the output?**
```javascript
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 1000);
}
```
-   **Answer:** `3, 3, 3`
-   **Why?** `var` is function-scoped. There is only **one** `i` in memory. By the time the `setTimeout` runs (after 1 second), the loop has already finished and `i` is 3.
-   **Fix:** Use `let i`. `let` is block-scoped, so a **new** `i` is created for every single turn of the loop.

---

## 🏗️ 2. The Coercion Confusion

**Q: What do these evaluate to?**
```javascript
console.log([] + []);   // "" (Empty String)
console.log([] + {});   // "[object Object]"
console.log(true + 1);  // 2 (true becomes 1)
console.log("5" - 1);   // 4 (subtraction converts to number)
console.log("5" + 1);   // "51" (addition converts to string)
```
-   **The Rule:** The `+` operator prefers **Strings**. The `-`, `*`, and `/` operators prefer **Numbers**.

---

## 🏗️ 3. The `forEach` Async Bug

**Q: Will this code wait for all items to be processed?**
```javascript
async function processAll(items) {
  items.forEach(async (item) => {
    await someAsyncAction(item);
  });
  console.log("Done!");
}
```
-   **Answer:** No. "Done!" will print almost immediately.
-   **Why?** `forEach` does **not** understand promises. It fires the functions and moves on without waiting.
-   **Fix:** Use a `for...of` loop or `Promise.all()`.

---

## 🏗️ 4. The `NaN` Paradox

**Q: What is the result?**
```javascript
console.log(typeof NaN); // "number"
console.log(NaN === NaN); // false
```
-   **Why?** In the IEEE floating-point standard, `NaN` (Not a Number) is technically a numeric type, but it is defined as being not equal to anything, including itself.

---

## 🏗️ 5. Closure & Reference Trap

**Q: What happens here?**
```javascript
let a = { name: "Nishant" };
let b = a;
a.name = "Rahul";

console.log(b.name); // "Rahul"
```
-   **Why?** Objects are passed by **Reference**. `a` and `b` both point to the same "box" in memory. If you change the contents of the box, both variables see the change.

---

## 🚀 Quick Tricky Facts Table

| Expression | Result | Why? |
| :--- | :--- | :--- |
| `0 == ""` | `true` | Both coerce to `0`. |
| `0 === ""` | `false` | Different types (Number vs String). |
| `null == undefined` | `true` | Defined as equal in the spec. |
| `null === undefined`| `false` | Different types. |
| `!!""` | `false` | Empty string is "falsy". |
| `!![]` | `true` | An empty array is "truthy". |

---

## 💼 Interview Tip: Think Out Loud

When given a tricky question, don't just guess. Explain the **mechanics**:
1.  "First, I see a `var` which is function-scoped..."
2.  "Next, `setTimeout` is a macrotask, so it goes to the queue..."
3.  "The loop finishes before the queue is touched..."

This shows you have **Deep Knowledge**, even if you get the final number wrong!

---

## 🔗 Navigation

**Prev:** [01_JS_Interview_Core.md](01_JS_Interview_Core.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [03_Coding_Problems.md](03_Coding_Problems.md)
