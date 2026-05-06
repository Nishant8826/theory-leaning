# 🚀 Interview Preparation - Javascript

> **Domain:** Web Development / Frontend & Backend  
> **Level:** Beginner to Expert  
> **Target Role:** Software Engineer / Senior Engineer / Lead

---

## 🟢 Beginner Level

### ❓ Q1. **What are the different data types in JavaScript?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Primitive types (Immutable, stored by value):** 
- `string`: Textual data.
- `number`: Double-precision 64-bit binary format IEEE 754.
- `boolean`: `true` or `false`.
- `null`: Intentional absence of value.
- `undefined`: Default value for uninitialized variables.
- `symbol`: Unique identifier.
- `bigint`: Arbitrary-precision integers.

**Non-primitive (Stored by reference):** 
- `object`: Key-value pairs, including arrays, functions, and dates.

> 💡 **Interviewer Focus:** Ensure mention of `symbol` and `bigint`. Clarify `typeof null` is `"object"` (a legacy bug).

</details>

<hr/>

### ❓ Q2. **What is the difference between `==` and `===`?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`==` (Loose Equality):** Performs **type coercion** before comparing. (e.g., `'5' == 5` is `true`).
- **`===` (Strict Equality):** Compares both **value and type** without coercion. (e.g., `'5' === 5` is `false`).

> 💡 **Interviewer Focus:** Coercion rules. Example: `[] == ![]` is `true` (very tricky). Use `===` by default for predictable code.

</details>

<hr/>

### ❓ Q3. **What is hoisting in JavaScript?**

<details>
<summary><b>👀 Show Answer</b></summary>

Hoisting is the behavior where variable and function declarations are moved to the top of their containing scope during the compilation phase.

- **`var`**: Hoisted and initialized with `undefined`.
- **`let`/`const`**: Hoisted but remain in the **Temporal Dead Zone (TDZ)**; accessing them before declaration throws a `ReferenceError`.
- **Function Declarations**: Fully hoisted (name and body).
- **Function Expressions**: Only the variable is hoisted (if using `var`), following variable rules.

> 💡 **Interviewer Focus:** Why TDZ exists (to prevent use-before-declaration bugs).

</details>

<hr/>

### ❓ Q4. **What is the difference between `var`, `let`, and `const`?**

<details>
<summary><b>👀 Show Answer</b></summary>

| Feature | `var` | `let` | `const` |
| :--- | :--- | :--- | :--- |
| **Scope** | Function Scope | Block Scope | Block Scope |
| **Hoisting** | Yes (`undefined`) | Yes (TDZ) | Yes (TDZ) |
| **Re-declaration**| Allowed | Not Allowed | Not Allowed |
| **Re-assignment** | Allowed | Allowed | Not Allowed |

> 💡 **Interviewer Focus:** Use `const` by default, `let` if the value changes, and avoid `var`.

</details>

<hr/>

### ❓ Q5. **Explain `null` vs `undefined`.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`undefined`**: A variable has been declared but has not yet been assigned a value.
- **`null`**: An assignment value that represents the intentional absence of any object value.

```javascript
typeof undefined // "undefined"
typeof null      // "object"
null == undefined  // true (equality)
null === undefined // false (identity)
```

</details>

<hr/>

### ❓ Q6. **What are template literals?**

<details>
<summary><b>👀 Show Answer</b></summary>

Template literals are string literals allowing embedded expressions. They use backticks (`` ` ``) instead of quotes.

- **Multiline strings:** No need for `\n`.
- **String Interpolation:** `${expression}`.
- **Tagged Templates:** Functions can parse template literals.

```javascript
const name = "JS";
console.log(`Hello, ${name}!`);
```

</details>

<hr/>

### ❓ Q7. **What is the difference between a function declaration and a function expression?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Declaration:** `function x() {}`. Hoisted entirely. Can be called before definition.
- **Expression:** `const x = function() {}`. Not hoisted (follows variable rules). Available only after the line it's defined.

> 💡 **Interviewer Focus:** Which one to use? Expressions are often preferred for arrow functions and keeping scope clean.

</details>

<hr/>

### ❓ Q8. **What are arrow functions and how do they differ from regular functions?**

<details>
<summary><b>👀 Show Answer</b></summary>

Introduced in ES6, arrow functions (`() => {}`) provide a concise syntax and:
1. **Lexical `this`**: They don't have their own `this`; they inherit it from the parent scope.
2. **No `arguments` object**: Use rest parameters instead.
3. **Cannot be used as constructors**: `new` will throw an error.
4. **No `prototype` property**.

</details>

<hr/>

### ❓ Q9. **What is the DOM?**

<details>
<summary><b>👀 Show Answer</b></summary>

The **Document Object Model (DOM)** is a programming interface for web documents. It represents the page so that programs can change the document structure, style, and content. It represents the HTML as a **tree of objects**.

</details>

<hr/>

### ❓ Q10. **How does type coercion work in JavaScript?**

<details>
<summary><b>👀 Show Answer</b></summary>

Type coercion is the automatic or implicit conversion of values from one data type to another. In JavaScript, this happens because it is a **weakly-typed** language.

#### 1. Implicit vs. Explicit Conversion
- **Explicit (Type Conversion):** When a developer intentionally converts a type.
  - `Number("10")`, `String(true)`, `Boolean(1)`.
- **Implicit (Type Coercion):** When JavaScript converts the type automatically during an operation.
  - `'5' - 2 // 3` (String to Number)
  - `'5' + 2 // "52"` (Number to String)

#### 2. Three Types of Coercion
JavaScript mainly coerces values to **Boolean**, **String**, or **Number**.

| Target Type | Triggered By | Logic |
| :--- | :--- | :--- |
| **Boolean** | Logical operators (`&&`, `||`, `!`) or control flow (`if`, `while`). | Uses **Truthy/Falsy** rules. |
| **String** | The binary `+` operator when at least one operand is a string. | All operands are converted to strings and concatenated. |
| **Number** | Math operators (`-`, `*`, `/`, `%`), comparison (`>`), or bitwise ops. | Values are converted to numbers. `true -> 1`, `false -> 0`, `null -> 0`, `undefined -> NaN`. |

#### 3. The `+` Operator Exception
The `+` operator is **overloaded**. It performs both addition and concatenation.
- If **any** operand is a string, it prefers **concatenation**.
- If **both** operands are numbers/booleans/null, it performs **addition**.

#### 4. Object to Primitive Conversion
When an object is used in a context where a primitive is expected (e.g., `obj + 1`), JavaScript follows the **`ToPrimitive`** algorithm:
1. It looks for `Symbol.toPrimitive(hint)`.
2. If not found, and hint is "string": calls `toString()`, then `valueOf()`.
3. If not found, and hint is "number" or "default": calls `valueOf()`, then `toString()`.

#### 5. Common "Gotchas" (The Weird Parts)
```javascript
true + false   // 1 (1 + 0)
12 / "6"       // 2
"number" + 15 + 3 // "number153"
15 + 3 + "number" // "18number"
[1] > null     // true (1 > 0)
"foo" + + "bar" // "fooNaN" (unary + "bar" is NaN)
[] + []        // "" (empty string)
[] + {}        // "[object Object]"
```

> 💡 **Interviewer Focus:** Coercion is why we use `===` (Strict Equality). It avoids the unpredictable results of implicit coercion that occur with `==`.

</details>

<hr/>

### ❓ Q11. **What are truthy and falsy values?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Falsy values:** `false`, `0`, `-0`, `0n` (BigInt zero), `""` (empty string), `null`, `undefined`, and `NaN`.
- **Truthy values:** Everything else, including `[]`, `{}`, and `"0"`.

</details>

<hr/>

### ❓ Q12. **What is the difference between `for...in` and `for...of`?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`for...in`**: Iterates over **enumerable property keys** (indices/names) of an object.
- **`for...of`**: Iterates over **values** of an iterable object (Array, Map, Set, String).

```javascript
const arr = [10, 20];
for (let i in arr) console.log(i); // 0, 1
for (let v of arr) console.log(v); // 10, 20
```

</details>

<hr/>

### ❓ Q13. **What are default parameters in ES6?**

<details>
<summary><b>👀 Show Answer</b></summary>

Allow named parameters to be initialized with default values if no value or `undefined` is passed.

```javascript
function greet(name = "Guest") {
  return `Hello ${name}`;
}
```

</details>

<hr/>

### ❓ Q14. **Explain the spread (`...`) and rest (`...`) operators.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Spread (`...`)**: Expands an iterable into individual elements. Used in array literals, object literals, or function calls.
- **Rest (`...`)**: Collects multiple elements into a single array. Used in function parameters or destructuring.

```javascript
const arr = [1, 2];
const newArr = [...arr, 3]; // Spread

function sum(...nums) { return nums.reduce((a, b) => a + b); } // Rest
```

</details>

<hr/>

### ❓ Q15. **What is destructuring assignment?**

<details>
<summary><b>👀 Show Answer</b></summary>

A syntax that allows unpacking values from arrays or properties from objects into distinct variables.

```javascript
const [a, b] = [1, 2];
const { name, age } = { name: "Alice", age: 25 };
```

</details>

<hr/>

### ❓ Q16. **How does `typeof` operator work? What are its quirks?**

<details>
<summary><b>👀 Show Answer</b></summary>

Returns a string indicating the type of the operand.
- `typeof 42` -> `"number"`
- `typeof "hi"` -> `"string"`
- `typeof true` -> `"boolean"`
- `typeof undefined` -> `"undefined"`
- **Quirk:** `typeof null` -> `"object"` (historical bug).
- **Quirk:** `typeof []` -> `"object"`.
- `typeof function(){}` -> `"function"`.

</details>

<hr/>

### ❓ Q17. **What is `NaN`? How do you check for it?**

<details>
<summary><b>👀 Show Answer</b></summary>

`NaN` stands for **Not-a-Number**. It is a property of the global object.
- **Quirk:** `typeof NaN` is `"number"`.
- `NaN === NaN` is `false`.
- **Check:** `Number.isNaN(value)` (preferred) or `isNaN(value)`.

</details>

<hr/>

### ❓ Q18. **What is the difference between `slice()`, `splice()`, and `split()`?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`slice(start, end)`**: Returns a shallow copy of a portion of an array. **Non-destructive**.
- **`splice(start, count, items)`**: Changes contents of an array by removing/replacing elements. **Destructive** (mutates original).
- **`split(separator)`**: A String method that splits a string into an array of substrings.

</details>

<hr/>

### ❓ Q19. **What is the difference between `map()`, `filter()`, and `reduce()`?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`map`**: Creates a new array with the results of calling a function on every element.
- **`filter`**: Creates a new array with all elements that pass the test implemented by the provided function.
- **`reduce`**: Executes a reducer function on each element, resulting in a **single output value**.

</details>

<hr/>

### ❓ Q20. **What is `"use strict"` and why would you use it?**

<details>
<summary><b>👀 Show Answer</b></summary>

A literal expression that enables **Strict Mode**.
- Prevents accidental globals (`x = 10;` throws error).
- Throws errors on silent failures (e.g., assigning to read-only props).
- Fixes mistakes that make it difficult for engines to optimize.
- Prohibits some syntax likely to be defined in future ES versions.

</details>

<hr/>

### ❓ Q21. **How does string comparison work in JavaScript?**

<details>
<summary><b>👀 Show Answer</b></summary>

Strings are compared **lexicographically** (based on Unicode values) using standard operators (`<`, `>`, `<=`, `>=`).

```javascript
"a" < "b" // true
"Z" < "a" // true (Uppercase comes before lowercase)
```

</details>

<hr/>

### ❓ Q22. **What are immediately invoked function expressions (IIFE)?**

<details>
<summary><b>👀 Show Answer</b></summary>

A function that runs as soon as it is defined.

```javascript
(function() {
  // Private scope
})();
```

> 🎯 **Use case:** Avoiding polluting the global namespace and creating private variables before ES6 modules existed.

</details>

<hr/>

### ❓ Q23. **What is scope in JavaScript? Explain the types.**

<details>
<summary><b>👀 Show Answer</b></summary>

Scope determines the visibility of variables.
1. **Global Scope:** Accessible everywhere.
2. **Function Scope:** Accessible only inside the function (`var`).
3. **Block Scope:** Accessible only inside `{}` (`let`, `const`).
4. **Lexical Scope:** Inner functions have access to variables defined in their outer scope.

</details>

<hr/>

### ❓ Q24. **What is the difference between `push()`/`pop()` and `shift()`/`unshift()`?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`push` / `pop`**: Add/Remove from the **end** of the array. (Fast: O(1)).
- **`shift` / `unshift`**: Remove/Add from the **beginning** of the array. (Slower: O(n) because elements must be re-indexed).

</details>

<hr/>

### ❓ Q25. **How do you clone an object in JavaScript?**

<details>
<summary><b>👀 Show Answer</b></summary>

1. **Shallow Copy:** `Object.assign({}, obj)` or `{ ...obj }`.
2. **Deep Copy:** `JSON.parse(JSON.stringify(obj))` (limitations with functions/dates) or `structuredClone(obj)` (Modern standard).

</details>
<br>

## 🟡 Intermediate Level

### ❓ Q26. **What are closures? Explain with an example.**

<details>
<summary><b>👀 Show Answer</b></summary>

A closure is a function that **remembers its outer scope** even after the outer function has returned.

```js
function counter() {
  let count = 0;
  return function() {
    return ++count;
  };
}
const inc = counter();
inc(); // 1
inc(); // 2
```

> ⚙️ **How it works:** When `counter()` returns, its execution context is destroyed but the inner function still holds a **reference** to the `count` variable via its `[[Environment]]` (closure). The variable is kept alive on the heap.

> 🎯 **Use cases:** Data privacy, function factories, partial application, module pattern.

> 💡 **Interviewer Focus:** Ask about memory implications. Closures can cause **memory leaks** if large objects are unintentionally retained.

</details>

<hr/>

### ❓ Q27. **Explain the `this` keyword in JavaScript.**

<details>
<summary><b>👀 Show Answer</b></summary>

`this` depends on **how** a function is called, not where it's defined:

| Context | `this` refers to |
|---------|-----------------|
| Global (non-strict) | `window` / `globalThis` |
| Global (strict) | `undefined` |
| Object method | The object |
| `new` Constructor | The new instance |
| `call/apply/bind` | Explicitly set |
| Arrow function | Lexical (enclosing scope) |
| Event handler | The DOM element |

> 💡 **Interviewer Focus:** Give a code snippet and ask what `this` is. Test arrow functions inside objects.

</details>

<hr/>

### ❓ Q28. **What is the prototype chain?**

<details>
<summary><b>👀 Show Answer</b></summary>

Every JS object has an internal `[[Prototype]]` link to another object. When a property is accessed, JS looks up the **prototype chain** until it finds the property or reaches `null`.

```
myObj → Object.prototype → null
myArr → Array.prototype → Object.prototype → null
```

`Object.create(proto)` creates an object with `proto` as its prototype.
`__proto__` is the accessor; `Object.getPrototypeOf()` is the standard way.

> 💡 **Interviewer Focus:** Difference between `__proto__` and `prototype` property. `prototype` exists only on functions.

</details>

<hr/>

### ❓ Q29. **Explain `call()`, `apply()`, and `bind()`.**

<details>
<summary><b>👀 Show Answer</b></summary>

All three explicitly set `this`:

```js
func.call(thisArg, arg1, arg2);     // Calls immediately, args as list
func.apply(thisArg, [arg1, arg2]);  // Calls immediately, args as array
const bound = func.bind(thisArg);   // Returns NEW function, doesn't call
```

> 🔑 **Key difference:** `bind()` returns a new function; `call()`/`apply()` invoke immediately.

</details>

<hr/>

### ❓ Q30. **What is the event loop? Explain the execution model.**

<details>
<summary><b>👀 Show Answer</b></summary>

JavaScript is **single-threaded**. The event loop enables async behavior:

1. **Call Stack** — Executes synchronous code (LIFO).
2. **Web APIs / Node APIs** — Handle async operations (timers, HTTP, DOM events).
3. **Callback Queue (Task Queue)** — Holds callbacks from completed async ops (macrotasks).
4. **Microtask Queue** — Holds `.then()`, `MutationObserver`, `queueMicrotask()` callbacks.

**Order:** Call Stack → **ALL Microtasks** → ONE Macrotask → ALL Microtasks → repeat.

```js
console.log('1');
setTimeout(() => console.log('2'), 0);
Promise.resolve().then(() => console.log('3'));
console.log('4');
// Output: 1, 4, 3, 2
```

> 💡 **Interviewer Focus:** Microtasks always drain before the next macrotask. Ask for output prediction.

</details>

<hr/>

### ❓ Q31. **What are Promises? Explain the states.**

<details>
<summary><b>👀 Show Answer</b></summary>

A Promise represents a **future value**. Three states:
- **Pending** — Initial state.
- **Fulfilled** — Operation succeeded (`.then()` fires).
- **Rejected** — Operation failed (`.catch()` fires).

Once settled (fulfilled/rejected), a promise is **immutable** — state cannot change.

```js
const p = new Promise((resolve, reject) => {
  // async work
  resolve(value); // or reject(error)
});
p.then(onFulfilled).catch(onRejected).finally(onSettled);
```

> 💡 **Interviewer Focus:** Ask about `Promise.all()` vs `Promise.allSettled()` vs `Promise.race()` vs `Promise.any()`.

</details>

<hr/>

### ❓ Q32. **What is `async/await` and how does it work under the hood?**

<details>
<summary><b>👀 Show Answer</b></summary>

`async/await` is syntactic sugar over Promises.

- `async` function always returns a Promise.
- `await` pauses execution of the async function, yielding control back to the event loop.

> 🔍 **Under the hood:** The engine transforms `await` into a `.then()` chain. The function is split at each `await` into microtask-scheduled continuations.

```js
async function fetchData() {
  try {
    const res = await fetch('/api');  // pauses here
    const data = await res.json();
    return data;
  } catch (err) {
    console.error(err);
  }
}
```

> 💡 **Interviewer Focus:** Common mistake — `await` in a loop (sequential). Use `Promise.all()` for parallel.

</details>

<hr/>

### ❓ Q33. **Explain event delegation and event bubbling.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Event Bubbling:** Events propagate from the target element **up** to the root. Phases: Capture → Target → Bubble.

**Event Delegation:** Attach a **single** listener to a parent, handle events from children using `event.target`.

```js
document.getElementById('list').addEventListener('click', (e) => {
  if (e.target.tagName === 'LI') {
    console.log(e.target.textContent);
  }
});
```

> ✨ **Benefits:** Memory efficient, handles dynamically added elements.

</details>

<hr/>

### ❓ Q34. **What is debouncing and throttling?**

<details>
<summary><b>👀 Show Answer</b></summary>

Both limit the rate of function execution:

**Debounce:** Executes after a **pause** in events. Resets timer on each call.
```js
function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}
```

**Throttle:** Executes at most **once** per interval.
```js
function throttle(fn, limit) {
  let inThrottle;
  return (...args) => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}
```

> 🎯 **Use cases:** Debounce → search input. Throttle → scroll/resize handlers.

</details>

<hr/>

### ❓ Q35. **What is the difference between shallow copy and deep copy?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Shallow Copy:** Copies the object's top-level properties. Nested objects still share the same reference. (`{...obj}`, `Object.assign()`).
- **Deep Copy:** Copies all levels of the object, creating new instances for nested objects. (`structuredClone()`, `JSON.parse(JSON.stringify(obj))`).

</details>

<hr/>

### ❓ Q36. **Explain `Object.freeze()`, `Object.seal()`, and `Object.preventExtensions()`.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`Object.preventExtensions(obj)`**: Prevents adding new properties.
- **`Object.seal(obj)`**: Prevents adding/removing properties. Existing properties can still be modified.
- **`Object.freeze(obj)`**: Prevents any changes (adding, removing, or modifying properties). **Immutable**.

</details>

<hr/>

### ❓ Q37. **What are higher-order functions?**

<details>
<summary><b>👀 Show Answer</b></summary>

A function that either:
1. Takes one or more functions as arguments.
2. Returns a function as its result.

Examples: `map`, `filter`, `reduce`, `setTimeout`.

</details>

<hr/>

### ❓ Q38. **What is currying in JavaScript?**

<details>
<summary><b>👀 Show Answer</b></summary>

Currying transforms a function with multiple arguments into a sequence of functions, each taking a single argument.

```js
// Normal
function add(a, b) { return a + b; }

// Curried
function add(a) {
  return function(b) {
    return a + b;
  };
}
add(2)(3); // 5

// Generic curry utility
const curry = (fn) => {
  const arity = fn.length;
  return function curried(...args) {
    if (args.length >= arity) return fn(...args);
    return (...next) => curried(...args, ...next);
  };
};
```

> 🎯 **Use cases:** Partial application, function composition, configuration.

</details>

<hr/>

### ❓ Q39. **What are `Map` and `Set` in ES6? How do they differ from objects/arrays?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`Map`**: Collection of keyed data items. Keys can be **any type** (including objects). Maintains insertion order.
- **`Set`**: Collection of **unique** values. No duplicates allowed.

**Vs Objects:** Maps have size property, keys can be anything, and they are directly iterable.

</details>

<hr/>

### ❓ Q40. **Explain `WeakMap` and `WeakSet`.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **WeakMap:** Keys must be **objects**. Keys are held **weakly** — if no other reference exists, they are garbage collected. Not iterable, no `.size`.
- **WeakSet:** Values must be **objects**. Weakly held. Not iterable.

> 🎯 **Use cases:** Storing metadata about objects without preventing GC. Private data, DOM node tracking, caching.

> 💡 **Interviewer Focus:** Why weak references matter for memory management.

</details>

<hr/>

### ❓ Q41. **What are generators in JavaScript?**

<details>
<summary><b>👀 Show Answer</b></summary>

Generators are functions that can be exited and later re-entered. They maintain their context (variable bindings) across re-entrances.
- Defined with `function*`.
- Use `yield` to pause execution.
- Return an iterator with a `next()` method.

```javascript
function* count() {
  yield 1;
  yield 2;
}
const g = count();
g.next(); // { value: 1, done: false }
```

</details>

<hr/>

### ❓ Q42. **Explain the module system — CommonJS vs ES Modules.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **CommonJS (CJS):** Node.js default. `require()` and `module.exports`. Synchronous.
- **ES Modules (ESM):** Modern standard. `import` and `export`. Asynchronous, supports **Tree Shaking** (removing unused code).

</details>

<hr/>

### ❓ Q43. **What is the difference between `Object.keys()`, `Object.values()`, and `Object.entries()`?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`Object.keys(obj)`**: Returns an array of enumerable **property names**.
- **`Object.values(obj)`**: Returns an array of enumerable **property values**.
- **`Object.entries(obj)`**: Returns an array of `[key, value]` pairs.

</details>

<hr/>

### ❓ Q44. **How does `JSON.parse()` and `JSON.stringify()` work? What are the limitations?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`stringify`**: Converts a JS object/value to a JSON string.
- **`parse`**: Parses a JSON string, constructing the JS value/object.
- **Limitations:** Cannot handle circular references, functions, Symbols, or `undefined` (they are omitted or converted to null).

</details>

<hr/>

### ❓ Q45. **What are Symbols and what are they used for?**

<details>
<summary><b>👀 Show Answer</b></summary>

A primitive type used to create **unique, anonymous identifiers** for object properties.
- `const sym = Symbol("description")`.
- **Use case:** Adding "hidden" properties to objects that don't collide with other keys and aren't visible in normal loops (`for...in`).

</details>

<hr/>

### ❓ Q46. **What is optional chaining (`?.`) and nullish coalescing (`??`)?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`?.`**: Short-circuits and returns `undefined` if the reference is `null` or `undefined`.
- **`??`**: Returns the right-hand operand only if the left-hand is `null` or `undefined`. (Unlike `||`, it treats `0` or `""` as truthy).

</details>

<hr/>

### ❓ Q47. **What is the difference between `setTimeout` and `setInterval`?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`setTimeout`**: Executes a function **once** after a delay.
- **`setInterval`**: Executes a function **repeatedly** with a fixed delay between each call.

</details>

<hr/>

### ❓ Q48. **What is memoization? Implement a basic memoize function.**

<details>
<summary><b>👀 Show Answer</b></summary>

An optimization technique that stores the results of expensive function calls and returns the cached result when the same inputs occur again.

```javascript
function memoize(fn) {
  const cache = {};
  return (...args) => {
    const key = JSON.stringify(args);
    return cache[key] || (cache[key] = fn(...args));
  };
}
```

</details>

<hr/>

### ❓ Q49. **How do you handle errors in Promises vs async/await?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Promises:** Use `.catch()` at the end of the chain.
- **Async/Await:** Use `try...catch` blocks around the awaited expressions.

</details>

<hr/>

### ❓ Q50. **What is the difference between composition and inheritance in JavaScript?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Inheritance:** Designing types based on what they **are** (A Car *is a* Vehicle). Uses `extends`.
- **Composition:** Designing types based on what they **do** (A Car *has an* Engine). Combining small, focused objects/functions to build complex ones. 

> 🚀 **Pro-tip:** "Favor composition over inheritance" for more flexible and maintainable code.

</details>

---

## 🔴 Advanced Level

### ❓ Q51. **Explain the JavaScript engine pipeline (parsing → execution).**

<details>
<summary><b>👀 Show Answer</b></summary>

1. **Tokenizing/Lexing** — Source code → tokens.
2. **Parsing** — Tokens → Abstract Syntax Tree (AST).
3. **Interpretation** — AST → bytecode (Ignition in V8).
4. **Optimization** — Hot functions → optimized machine code (TurboFan in V8).
5. **Deoptimization** — If assumptions fail, falls back to bytecode.

V8's pipeline: `Source → Parser → AST → Ignition (bytecode) → TurboFan (optimized code)`

> 💡 **Interviewer Focus:** Ask about hidden classes, inline caching, and what causes deoptimization (changing object shape, polymorphic call sites).

</details>

<hr/>

### ❓ Q52. **What are hidden classes and inline caches in V8?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Hidden Classes (Maps in V8):** V8 assigns a hidden class to every object to optimize property access. Objects with the same structure share the same hidden class.

```js
// Same hidden class — fast
function Point(x, y) { this.x = x; this.y = y; }
const p1 = new Point(1, 2);
const p2 = new Point(3, 4);

// Different hidden classes — slow (adding props in different order)
const a = {}; a.x = 1; a.y = 2;
const b = {}; b.y = 1; b.x = 2; // different transition chain
```

**Inline Caching (IC):** Caches the lookup location of properties. Monomorphic (1 shape) → fast. Polymorphic (2-4) → slower. Megamorphic (5+) → slowest.

> 💡 **Interviewer Focus:** Always initialize object properties in the same order. Avoid adding/deleting properties dynamically.

</details>

<hr/>

### ❓ Q53. **Explain `Proxy` and `Reflect` in JavaScript.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Proxy:** Creates a wrapper around an object that intercepts operations (get, set, delete, etc.).

```js
const handler = {
  get(target, prop) {
    return prop in target ? target[prop] : `Property ${prop} not found`;
  },
  set(target, prop, value) {
    if (typeof value !== 'number') throw TypeError('Must be number');
    target[prop] = value;
    return true;
  }
};
const obj = new Proxy({}, handler);
```

**Reflect:** Provides default behavior for proxy traps. Mirror of Proxy trap methods.

```js
Reflect.get(target, prop);
Reflect.set(target, prop, value);
```

> 🎯 **Use cases:** Validation, logging, reactive systems (Vue 3), access control, negative array indexing.

</details>

<hr/>

### ❓ Q54. **How does garbage collection work in JavaScript?**

<details>
<summary><b>👀 Show Answer</b></summary>

V8 uses a **generational garbage collector**:

**Young Generation (Scavenger/Minor GC):**
- Small, frequently collected.
- Uses **semi-space** algorithm (from-space → to-space).
- Objects that survive 2 GC cycles are promoted to Old Generation.

**Old Generation (Mark-Sweep-Compact/Major GC):**
- Larger, less frequent.
- **Mark:** Traverse from roots, mark reachable objects.
- **Sweep:** Free unmarked objects.
- **Compact:** Defragment memory.

**Roots:** Global object, stack variables, active closures.

> 💧 **Common leaks:** Forgotten timers, detached DOM nodes, closures retaining large scopes, global variables.

> 💡 **Interviewer Focus:** Ask candidate to identify memory leaks in code snippets.

</details>

<hr/>

### ❓ Q55. **What is the Temporal Dead Zone (TDZ) in detail?**

<details>
<summary><b>👀 Show Answer</b></summary>

The TDZ is the region between the **start of the scope** and the **declaration line** for `let`/`const`. Accessing the variable in TDZ throws `ReferenceError`.

```js
{
  // TDZ starts for `x`
  console.log(x); // ReferenceError
  let x = 10;     // TDZ ends
}
```

**Why it exists:** Prevents use-before-declaration bugs. `var` hoisting to `undefined` was a source of subtle bugs.

> 🧐 **Nuance:** TDZ applies per-scope. `typeof` on a TDZ variable also throws (unlike undeclared variables).

</details>

<hr/>

### ❓ Q56. **Explain `Object.create()` vs constructor functions vs `class`.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`Object.create(proto)`**: Creates a new object with the specified prototype. No constructor logic is run.
- **Constructor Function**: `function Person() {}`. Used with `new`. Sets `this`, returns an object, and links `prototype`.
- **`class`**: Syntactic sugar over constructor functions and prototypes. Supports `extends`, `super`, and static methods.

</details>

<hr/>

### ❓ Q57. **What are tagged template literals?**

<details>
<summary><b>👀 Show Answer</b></summary>

A more advanced form of template literals where you can parse template literals with a function.

```javascript
function highlight(strings, ...values) {
  return strings.reduce((acc, str, i) => `${acc}${str}<b>${values[i] || ""}</b>`, "");
}
const name = "JS";
highlight`Hello ${name}`; // "Hello <b>JS</b>"
```

</details>

<hr/>

### ❓ Q58. **Explain `Symbol.iterator` and the iterable protocol.**

<details>
<summary><b>👀 Show Answer</b></summary>

An object is **iterable** if it implements `[Symbol.iterator]()` returning an **iterator** (object with `next()` method).

```js
const range = {
  from: 1,
  to: 5,
  [Symbol.iterator]() {
    let current = this.from;
    const last = this.to;
    return {
      next() {
        return current <= last
          ? { value: current++, done: false }
          : { done: true };
      }
    };
  }
};

for (const n of range) console.log(n); // 1, 2, 3, 4, 5
```

**Built-in iterables:** Array, String, Map, Set, TypedArray, `arguments`, NodeList.

> 💡 **Interviewer Focus:** How `for...of`, spread, and destructuring all use the iterable protocol internally.

</details>

<hr/>

### ❓ Q59. **What is `SharedArrayBuffer` and `Atomics`?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`SharedArrayBuffer`**: Allows sharing memory between the main thread and web workers.
- **`Atomics`**: A global object that provides atomic operations (like `add`, `sub`, `wait`, `notify`) to ensure thread-safe access to shared memory.

</details>

<hr/>

### ❓ Q60. **Explain structured cloning vs `JSON.parse(JSON.stringify())`.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`JSON` method**: Simple but loses types like `Map`, `Set`, `Date`, `RegExp`, and fails on circular references.
- **Structured Cloning (`structuredClone`)**: Native API that handles circular references and almost all built-in types (`Map`, `Set`, `Date`, `Buffer`, etc.). It still cannot clone functions or DOM nodes.

</details>

<hr/>

### ❓ Q61. **What are `WeakRef` and `FinalizationRegistry`?**

<details>
<summary><b>👀 Show Answer</b></summary>

**`WeakRef`** (ES2021): Holds a weak reference to an object — doesn't prevent GC.

```js
let obj = { data: "important" };
const ref = new WeakRef(obj);
ref.deref(); // returns obj or undefined if GC'd
```

**`FinalizationRegistry`**: Callback when a registered object is GC'd.

```js
const registry = new FinalizationRegistry((value) => {
  console.log(`${value} was garbage collected`);
});
registry.register(obj, "my object");
```

> 🎯 **Use cases:** Caches, large resource management. Use sparingly — GC timing is non-deterministic.

</details>

<hr/>

### ❓ Q62. **How does `async` iteration (`for await...of`) work?**

<details>
<summary><b>👀 Show Answer</b></summary>

Allows iterating over asynchronous data sources (e.g., streams or arrays of promises).

```javascript
for await (const chunk of asyncIterable) {
  console.log(chunk);
}
```

It waits for each promise to resolve before moving to the next iteration.

</details>

<hr/>

### ❓ Q63. **What are private class fields (`#`) and how do they differ from closures for privacy?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`#` Fields**: Hard-coded private properties in a class. They are truly private and inaccessible from outside the class instance.
- **Closures**: Use scope to hide variables. Closures are more flexible but can lead to higher memory usage if not handled correctly.

</details>

<hr/>

### ❓ Q64. **Explain the `Intl` API and its use cases.**

<details>
<summary><b>👀 Show Answer</b></summary>

The **Internationalization API** provides language-sensitive string comparison, number formatting, and date/time formatting.
- `Intl.DateTimeFormat`
- `Intl.NumberFormat` (e.g., currency formatting)
- `Intl.Collator`

</details>

<hr/>

### ❓ Q65. **What is `queueMicrotask()` and when would you use it?**

<details>
<summary><b>👀 Show Answer</b></summary>

Explicitly adds a task to the microtask queue.
- **Use case:** When you want to ensure a function runs after the current task finishes but before the browser renders or the next macrotask starts. Similar to `Promise.resolve().then()`.

</details>

<hr/>

### ❓ Q66. **How does `structuredClone()` work and what are its limitations?**

<details>
<summary><b>👀 Show Answer</b></summary>

It uses the structured clone algorithm to create a deep copy.
- **Can clone:** Arrays, Objects, Dates, RegExps, Map, Set, Blobs, etc.
- **Cannot clone:** Functions, DOM nodes, Property descriptors, Getters/Setters.

</details>

<hr/>

### ❓ Q67. **What is tail call optimization (TCO)? Does V8 support it?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **TCO**: An optimization where the stack frame of a function is reused if the last action is a call to another function. Prevents stack overflow in recursion.
- **Support**: It is part of the ES6 spec but currently only **Safari (JSC)** supports it. V8 (Chrome/Node) does not support it for general use.

</details>

<hr/>

### ❓ Q68. **Explain `ArrayBuffer`, `TypedArray`, and `DataView`.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`ArrayBuffer`**: A generic, fixed-length raw binary data buffer.
- **`TypedArray`**: A view (like `Uint8Array`) that interprets the buffer as a specific type.
- **`DataView`**: A low-level interface for reading/writing multiple number types in an `ArrayBuffer` regardless of the platform's endianness.

</details>

<hr/>

### ❓ Q69. **What is the difference between `Object.assign()` and spread for cloning?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`Object.assign`**: Mutates the target object and triggers setters.
- **Spread (`...`)**: Always creates a new object and doesn't trigger setters (it defines new properties).

</details>

<hr/>

### ❓ Q70. **How do you implement the observer pattern in JavaScript?**

<details>
<summary><b>👀 Show Answer</b></summary>

Typically implemented with an object that maintains a list of dependents (observers) and notifies them of state changes.

```javascript
class Subject {
  constructor() { this.observers = []; }
  subscribe(fn) { this.observers.push(fn); }
  notify(data) { this.observers.forEach(fn => fn(data)); }
}
```

</details>

<hr/>

### ❓ Q71. **What are `AbortController` and `AbortSignal`?**

<details>
<summary><b>👀 Show Answer</b></summary>

`AbortController` creates a signal to cancel async operations (fetch, event listeners, streams).

```js
const controller = new AbortController();
const { signal } = controller;

fetch('/api', { signal })
  .then(res => res.json())
  .catch(err => {
    if (err.name === 'AbortError') console.log('Fetch aborted');
  });

// Cancel after 5 seconds
setTimeout(() => controller.abort(), 5000);
```

**Modern usage:** `AbortSignal.timeout(5000)` — built-in timeout signal. Can be used with `addEventListener` for cleanup.

</details>

<hr/>

### ❓ Q72. **Explain prototype pollution and how to prevent it.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Problem**: When an attacker injects properties into `Object.prototype`, affecting all objects in the application. Often happens via unsafe merging or cloning.
- **Prevention**: Use `Object.create(null)` for maps, freeze the prototype, or use Map/Set instead of plain objects.

</details>

<hr/>

### ❓ Q73. **What is the `Temporal` API proposal and what problems does it solve?**

<details>
<summary><b>👀 Show Answer</b></summary>

A modern replacement for the `Date` object.
- **Fixes**: Mutability, poor timezone support, difficult arithmetic, and the fact that `Date` is based on Java's `java.util.Date` which is widely considered broken.

</details>

<hr/>

### ❓ Q74. **How does `Promise.allSettled()` differ from `Promise.all()`?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`Promise.all()`**: Short-circuits and rejects if **any** promise rejects.
- **`Promise.allSettled()`**: Waits for **all** promises to settle (either fulfilled or rejected) and returns an array of results with their status.

</details>

<hr/>

### ❓ Q75. **What is a service worker and how does its lifecycle work?**

<details>
<summary><b>👀 Show Answer</b></summary>

A script that the browser runs in the background, separate from a web page, enabling features like push notifications and offline support.
- **Lifecycle**: Registration -> Installation -> Activation.

</details>

---

## 🟣 Expert Level

### ❓ Q76. **Explain V8's Ignition interpreter and TurboFan compiler pipeline in depth.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Ignition (Interpreter):**
- Compiles AST → compact **bytecode**.
- Executes bytecode using a register-based interpreter.
- Collects **type feedback** (ICs) during execution.

**Sparkplug (Baseline Compiler — V8 v9.1+):**
- Non-optimizing compiler between Ignition and TurboFan.
- Quickly compiles bytecode → machine code without optimization.

**TurboFan (Optimizing Compiler):**
- Uses type feedback from Ignition to generate **optimized machine code**.
- Performs speculative optimization (assumes types won't change).
- Optimizations: inlining, escape analysis, dead code elimination, loop unrolling.

**Deoptimization:** If speculative assumptions break (type changes, hidden class transitions), TurboFan **deoptimizes** back to Ignition bytecode.

> 🚫 **Anti-patterns:** Polymorphic functions, changing object shapes, `arguments` leaking, `eval()`, `with`, `delete`.

</details>

<hr/>

### ❓ Q77. **How does the Mark-Compact garbage collector handle large heaps in V8?**

<details>
<summary><b>👀 Show Answer</b></summary>

For large heaps, V8 uses:

1. **Incremental Marking:** Instead of stop-the-world, marking is split into small steps interleaved with JS execution. Uses a **tri-color** marking scheme (white/grey/black) with a write barrier to track mutations during marking.

2. **Concurrent Marking:** Marking happens on **helper threads** concurrently with the main thread.

3. **Concurrent Sweeping:** Sweep phase also runs on background threads.

4. **Parallel Compaction:** Memory compaction runs on multiple threads.

5. **Lazy Sweeping:** Pages are swept on-demand when allocation needs them.

**Orinoco** is V8's GC project name — goal is near-zero pause time GC.

> 💡 **Interviewer Focus:** How incremental/concurrent GC reduces pause times. Write barrier cost vs throughput.

</details>

<hr/>

### ❓ Q78. **Explain the microtask checkpoint algorithm in detail.**

<details>
<summary><b>👀 Show Answer</b></summary>

After each **macrotask** (and other specific checkpoints), the engine runs the microtask checkpoint:

1. While the microtask queue is not empty:
   a. Dequeue the oldest microtask.
   b. Execute it.
   c. If it enqueues new microtasks, they are added to the **same queue**.
2. Repeat until the microtask queue is **completely drained**.
3. Only then proceed to rendering or the next macrotask.

**Critical implications:**
- An infinite microtask loop **blocks rendering and macrotasks forever**.
- `process.nextTick()` in Node.js runs before Promise microtasks.
- In browsers: Microtask checkpoint also runs after each `MutationObserver` callback.

```js
Promise.resolve().then(function loop() {
  Promise.resolve().then(loop); // Infinite microtask loop — page freezes
});
```

</details>

<hr/>

### ❓ Q79. **What is speculative optimization and how does V8 use type feedback?**

<details>
<summary><b>👀 Show Answer</b></summary>

Speculative optimization is where the JIT compiler makes assumptions about the types of variables based on previous execution data (**Type Feedback**).
- V8 collects feedback in Inline Caches (ICs).
- If a function is called many times with integers, TurboFan generates machine code optimized specifically for integers.
- If it's later called with a string, the assumption is violated, and the code **deoptimizes** (bailout).

</details>

<hr/>

### ❓ Q80. **Explain JavaScript's memory layout — stack vs heap, closures, and hidden classes.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Stack**: Stores primitive values and references to objects. Managed by the OS (LIFO).
- **Heap**: Large, unstructured memory pool for objects and closures. Managed by GC.
- **Closures**: Variables captured by closures are stored on the **Heap** (in a Context object) because they must outlive the function's execution stack frame.
- **Hidden Classes**: Metadata stored in the Heap to describe the "shape" of an object.

</details>

<hr/>

### ❓ Q81. **What are Realms in JavaScript and how do they affect `instanceof`?**

<details>
<summary><b>👀 Show Answer</b></summary>

A **Realm** is an isolated JavaScript execution environment with its own global object and set of built-in objects. Each `<iframe>`, worker, or `vm.createContext()` (Node) creates a new Realm.

**`instanceof` problem across Realms:**
```js
// iframe's Array !== parent's Array
const arr = iframeWindow.document.createElement('div');
arr instanceof Array; // false! Different Array constructor
```

> 🛠️ **Solutions:** `Array.isArray()` works cross-realm. Check `Symbol.toStringTag` or `Object.prototype.toString.call()`.

</details>

<hr/>

### ❓ Q82. **How do you implement a custom async iterator?**

<details>
<summary><b>👀 Show Answer</b></summary>

By implementing the `[Symbol.asyncIterator]` method that returns an object with a `next()` method returning a promise of `{ value, done }`.

```javascript
const asyncIterable = {
  [Symbol.asyncIterator]() {
    let i = 0;
    return {
      async next() {
        if (i < 3) return { value: i++, done: false };
        return { done: true };
      }
    };
  }
};
```

</details>

<hr/>

### ❓ Q83. **Explain the module evaluation and linking phases of ES Modules.**

<details>
<summary><b>👀 Show Answer</b></summary>

1. **Construction**: Fetching, parsing, and creating Module Records.
2. **Instantiation**: Linking exports to imports. Finding boxes in memory for all exported values (but not filling them yet).
3. **Evaluation**: Running the code to fill those boxes with actual values.

**Key:** ESM is "live linked"—imports point to the actual memory location of the export, not a copy.

</details>

<hr/>

### ❓ Q84. **What is the cost model of JavaScript closures — when do they cause memory issues?**

<details>
<summary><b>👀 Show Answer</b></summary>

Closures capture the **entire variable environment** of their enclosing scope (in most engines, V8 optimizes this to only captured variables).

**Memory issues occur when:**
1. A closure captures a variable pointing to a large object, even if the closure doesn't use the large object.
2. Long-lived closures (event handlers, intervals) hold references preventing GC.
3. Multiple closures from the same scope share the same closure scope — if ANY of them is alive, ALL captured variables stay alive.

```js
function outer() {
  const bigData = new Array(1000000);
  const smallData = 'hello';
  
  // Both closures share scope — bigData stays alive
  // even though only `getSmall` survives
  const getBig = () => bigData;
  const getSmall = () => smallData;
  
  return getSmall; // bigData is NOT GC'd in many engines
}
```

> 💡 **Interviewer Focus:** V8 performs context specialization — only captures used variables. But shared context between multiple closures can retain more than expected.

</details>

<hr/>

### ❓ Q85. **How does `Reflect.construct()` differ from `new` and what's its use with Proxy?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`Reflect.construct(target, args, newTarget)`**: Equivalent to `new target(...args)` but allows you to specify a different constructor to be the prototype of the new object.
- **Use with Proxy**: Essential when implementing `construct` traps to ensure the `new.target` and prototype chain are correctly preserved.

</details>

<hr/>

### ❓ Q86. **Explain the difference between enumerable, configurable, and writable property descriptors.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Enumerable**: If `true`, the property shows up in `for...in` and `Object.keys()`.
- **Configurable**: If `false`, the property cannot be deleted and its descriptors (except `writable`) cannot be changed.
- **Writable**: If `false`, the property value cannot be changed.

</details>

<hr/>

### ❓ Q87. **What are the security implications of `eval()`, `Function()`, and `innerHTML`?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`eval()` / `Function()`**: XSS (Cross-Site Scripting) risk. They execute strings as code, which can be manipulated by attackers.
- **`innerHTML`**: Also an XSS risk as it parses HTML tags, potentially executing `<script>` or `onerror` handlers. Use `textContent` or `innerText` instead.

</details>

<hr/>

### ❓ Q88. **How do you detect and fix memory leaks in a production JavaScript application?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Detection:**
1. **Chrome DevTools Heap Snapshots** — Compare snapshots over time, look for growing retained size.
2. **Allocation Timeline** — Record allocations and identify objects not being freed.
3. **`performance.measureUserAgentSpecificMemory()`** — API for production monitoring.
4. **Node.js:** `--inspect` + Chrome DevTools, `process.memoryUsage()`, `v8.getHeapStatistics()`.

> 💧 **Common leak patterns:** - Detached DOM trees (DOM nodes removed from tree but referenced in JS).
- Closures retaining large scopes.
- Forgotten `setInterval`/`addEventListener`.
- Growing Maps/Sets/arrays that are never pruned.
- Console references (DevTools holds refs to logged objects).

> 🔧 **Fix approach:** 1. Nullify references when done.
2. Use `WeakMap`/`WeakSet` for metadata.
3. `removeEventListener` / `clearInterval` on cleanup.
4. Use `AbortController` for event listener cleanup.

</details>

<hr/>

### ❓ Q89. **Explain the difference between the task queue, microtask queue, and requestAnimationFrame.**

<details>
<summary><b>👀 Show Answer</b></summary>

1. **Microtask Queue**: Promises, MutationObserver. Runs immediately after the current task and before the next task.
2. **requestAnimationFrame (rAF)**: Runs before the next paint/render. Ideal for animations.
3. **Task Queue (Macrotask)**: `setTimeout`, `setInterval`, events. Runs after the browser has had a chance to render (usually).

</details>

<hr/>

### ❓ Q90. **What is `import()` dynamic import and how does code splitting work?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`import()`**: Returns a promise that resolves to the module object. Allows loading code on-demand.
- **Code Splitting**: Bundlers (like Webpack/Vite) detect dynamic imports and create separate chunks (files). These are only downloaded when the `import()` is called, reducing initial load time.

</details>

<hr/>

### ❓ Q91. **How does V8's optimizing compiler handle polymorphic vs monomorphic call sites?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Monomorphic**: Always sees the same hidden class. Very fast, can be **inlined**.
- **Polymorphic**: Sees 2-4 different hidden classes. Slower, uses a small table lookup.
- **Megamorphic**: Sees 5+ hidden classes. Very slow, falls back to a global lookup table.

</details>

<hr/>

### ❓ Q92. **What is zone.js and how does Angular use it to detect changes?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **`zone.js`**: Patches all async APIs (setTimeout, fetch, etc.) to track when they start and finish.
- **Angular**: Uses a Zone to know exactly when an async operation has finished, so it can automatically trigger change detection and update the DOM.

</details>

<hr/>

### ❓ Q93. **Explain the structured clone algorithm — what can and cannot be cloned?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Can**: Primitive types, Array, Object, Map, Set, Date, RegExp, ArrayBuffer, Blob, ImageBitmap.
- **Cannot**: Functions, DOM nodes, Error objects (partially), Property getters/setters, `Symbol`s.

</details>

<hr/>

### ❓ Q94. **How does `with` statement work and why is it banned in strict mode?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **How**: Extends the scope chain for a statement.
- **Problem**: Makes code ambiguous and hard to read. Prevents engines from performing static analysis/optimizations because it's unclear where a variable belongs at compile time.

</details>

<hr/>

### ❓ Q95. **What are the implications of `Object.freeze()` on V8's hidden class transitions?**

<details>
<summary><b>👀 Show Answer</b></summary>

Freezing an object creates a new hidden class that marks all properties as non-writable and non-configurable. It prevents further transitions but can lead to slightly better performance for property reads since the engine knows they will never change.

</details>

<hr/>

### ❓ Q96. **How do you implement a proper deep equality check in JavaScript?**

<details>
<summary><b>👀 Show Answer</b></summary>

By recursively comparing keys and values.

```javascript
function isDeepEqual(obj1, obj2) {
  if (obj1 === obj2) return true;
  if (typeof obj1 !== 'object' || obj1 === null || typeof obj2 !== 'object' || obj2 === null) return false;
  const keys1 = Object.keys(obj1), keys2 = Object.keys(obj2);
  if (keys1.length !== keys2.length) return false;
  for (let key of keys1) {
    if (!keys2.includes(key) || !isDeepEqual(obj1[key], obj2[key])) return false;
  }
  return true;
}
```

</details>

<hr/>

### ❓ Q97. **Explain the observable pattern using Proxy traps (like Vue 3's reactivity system).**

<details>
<summary><b>👀 Show Answer</b></summary>

Vue 3 uses `Proxy` to create reactive objects:

```js
function reactive(target) {
  const subscribers = new Map();
  
  return new Proxy(target, {
    get(obj, prop) {
      // Track: register current effect as dependency
      track(subscribers, prop);
      const value = Reflect.get(obj, prop);
      return typeof value === 'object' ? reactive(value) : value;
    },
    set(obj, prop, value) {
      const result = Reflect.set(obj, prop, value);
      // Trigger: notify all subscribers of this prop
      trigger(subscribers, prop);
      return result;
    }
  });
}
```

> 🔑 **Key concepts:** - **Track:** During rendering, property accesses register the current component as a subscriber.
- **Trigger:** On set, all subscribers are re-executed.
- **Deep reactivity:** Nested objects are recursively wrapped (lazy in Vue 3).
- **Advantage over `Object.defineProperty` (Vue 2):** Handles new properties, array mutations, Map/Set natively.

</details>

<hr/>

### ❓ Q98. **What is the TC39 process and how do JavaScript features get standardized?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Stage 0 (Strawman)**: Initial idea.
- **Stage 1 (Proposal)**: Formal document.
- **Stage 2 (Draft)**: Precise description with spec text.
- **Stage 3 (Candidate)**: Spec complete, awaiting implementation feedback.
- **Stage 4 (Finished)**: Ready for inclusion in the official ECMA standard.

</details>

<hr/>

### ❓ Q99. **How do JavaScript engines handle tail calls and what is proper tail position?**

<details>
<summary><b>👀 Show Answer</b></summary>

A call is in **Proper Tail Position** if it's the very last action of a function. The engine *could* reuse the current stack frame.
- However, as noted before, only Safari's JSC engine currently implements this. V8 chose not to due to debugging complexities and stack trace preservation.

</details>

<hr/>

### ❓ Q100. **Explain how `eval()` affects scope chain optimization and why it prevents many V8 optimizations.**

<details>
<summary><b>👀 Show Answer</b></summary>

`eval()` can introduce new variables into the current scope at runtime, making static analysis impossible.

**Impact on V8:**
1. **No scope optimization:** Normally V8 can statically determine which variables a closure needs. With `eval()`, any variable might be accessed, so ALL variables in the scope chain must be kept alive.
2. **No inlining:** Functions containing `eval()` cannot be inlined by TurboFan.
3. **Context allocation:** All local variables must be heap-allocated (on the context object), not stack-allocated.
4. **Deoptimization:** Functions in the scope chain of `eval()` cannot be optimized.

```js
function outer() {
  let x = 10, y = 20, z = 30; // ALL kept alive because of eval
  function inner(code) {
    eval(code); // Could access x, y, or z
  }
  return inner;
}
```

**Alternatives:** `new Function()` executes in global scope (less harmful). `JSON.parse()` for data.

**Indirect eval:** `(0, eval)('code')` runs in global scope, doesn't affect local optimization.

</details>

---

### 🧭 Navigation

| ⬅️ Previous | 🏠 Index | ➡️ Next |
| :--- | :---: | ---: |
| 🚫 *None* | [Home](./00_Index.md) | 🚫 *None* |
