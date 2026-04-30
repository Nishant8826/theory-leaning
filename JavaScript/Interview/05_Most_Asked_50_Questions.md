# 📌 05 — Top 50 Most Asked JavaScript Interview Questions

## 🌟 Introduction

These are the **most frequently asked** JavaScript interview questions across companies like Google, Amazon, Microsoft, Flipkart, and top startups. Each answer includes the **"Why it matters"** section to help you stand out.

---

## 📂 Category 1: Core Language Fundamentals

### Q1. What is the difference between `var`, `let`, and `const`?

| Feature | `var` | `let` | `const` |
| :--- | :--- | :--- | :--- |
| Scope | Function | Block | Block |
| Hoisting | Yes (initialized as `undefined`) | Yes (but in TDZ) | Yes (but in TDZ) |
| Re-declaration | ✅ Allowed | ❌ No | ❌ No |
| Re-assignment | ✅ Allowed | ✅ Allowed | ❌ No |

```javascript
// TDZ (Temporal Dead Zone) Demo
console.log(a); // undefined (var is hoisted)
console.log(b); // ReferenceError (let is in TDZ)
var a = 1;
let b = 2;
```

**Why it matters:** Companies test this to check if you understand scoping bugs in legacy codebases.

---

### Q2. Explain `==` vs `===` (Abstract vs Strict Equality)

- `==` performs **type coercion** before comparing.
- `===` compares **value AND type** without coercion.

```javascript
0 == ''        // true  (both coerce to 0)
0 === ''       // false (number vs string)
null == undefined  // true  (spec says so)
null === undefined // false (different types)
NaN == NaN     // false (NaN is never equal to anything)
```

**Rule:** Always use `===` unless you explicitly need coercion (e.g., `x == null` to check both `null` and `undefined`).

---

### Q3. What are JavaScript data types?

**Primitive Types (7):** `string`, `number`, `bigint`, `boolean`, `undefined`, `null`, `symbol`

**Reference Type (1):** `object` (includes arrays, functions, dates, regex, etc.)

```javascript
// Gotcha: typeof quirks
typeof null        // "object" (historical bug)
typeof []          // "object" (arrays are objects)
typeof function(){} // "function" (special case)
typeof NaN         // "number" (NaN is a numeric type)
typeof undefined   // "undefined"
typeof Symbol()    // "symbol"
typeof 10n         // "bigint"
```

---

### Q4. What is the difference between `null` and `undefined`?

| Aspect | `undefined` | `null` |
| :--- | :--- | :--- |
| Meaning | Variable declared but not assigned | Intentional "no value" |
| Type | `undefined` | `object` (bug) |
| Default | Function params, uninitialized vars | Developer assigns explicitly |

```javascript
let x;           // x is undefined
let y = null;    // y is intentionally empty
console.log(x == y);  // true (loose equality)
console.log(x === y); // false (different types)
```

---

### Q5. Explain Hoisting in detail.

**Hoisting** is JavaScript's behavior of moving declarations to the top of their scope during the **compilation phase**.

```javascript
// What you write:
console.log(greet); // undefined (var is hoisted)
sayHello();         // ✅ Works (function declaration is fully hoisted)
sayBye();           // ❌ TypeError (variable hoisted, not the function)

var greet = "Hi";
function sayHello() { console.log("Hello"); }
var sayBye = function() { console.log("Bye"); };
```

**Key Insight:** Only **declarations** are hoisted, not **initializations**. Function declarations are fully hoisted (name + body), but function expressions are treated like variables.

---

### Q6. What are Closures? Give a real-world use case.

A **closure** is when a function retains access to its **lexical scope** even after the outer function has returned.

```javascript
// Real-world: Creating private variables
function createCounter() {
  let count = 0; // Private — can't be accessed from outside
  return {
    increment: () => ++count,
    decrement: () => --count,
    getCount: () => count,
  };
}

const counter = createCounter();
counter.increment(); // 1
counter.increment(); // 2
counter.getCount();  // 2
// count is NOT accessible here — true encapsulation!
```

**Real-world uses:** Data privacy, memoization, partial application, event handlers with state.

---

### Q7. Explain `this` keyword with all binding rules.

```javascript
// Rule 1: Default Binding
function show() { console.log(this); }
show(); // window (non-strict) / undefined (strict)

// Rule 2: Implicit Binding
const obj = { name: "JS", show() { console.log(this.name); } };
obj.show(); // "JS"

// Rule 3: Explicit Binding
function greet() { console.log(this.name); }
greet.call({ name: "Call" });  // "Call"
greet.apply({ name: "Apply" }); // "Apply"
const bound = greet.bind({ name: "Bind" });
bound(); // "Bind"

// Rule 4: Arrow functions — NO own this
const obj2 = {
  name: "Arrow",
  show: () => console.log(this.name), // inherits from outer scope
};
obj2.show(); // undefined (this = window/global, not obj2)

// Rule 5: new Binding
function Person(name) { this.name = name; }
const p = new Person("Nishant"); // this = new empty object
```

**Priority Order:** `new` > `bind/call/apply` > Implicit (obj.method) > Default

---

### Q8. What is the Event Loop? Explain with example.

```
┌──────────────────────────┐
│       Call Stack          │  ← Runs synchronous code
└────────────┬─────────────┘
             │ (empty?)
             ▼
┌──────────────────────────┐
│    Microtask Queue        │  ← Promises, queueMicrotask, MutationObserver
│    (Runs ALL before next) │
└────────────┬─────────────┘
             │ (empty?)
             ▼
┌──────────────────────────┐
│    Macrotask Queue        │  ← setTimeout, setInterval, I/O, UI events
│    (Runs ONE, then check) │
└──────────────────────────┘
```

```javascript
console.log('1');                          // Sync
setTimeout(() => console.log('2'), 0);     // Macrotask
Promise.resolve().then(() => console.log('3')); // Microtask
queueMicrotask(() => console.log('4'));    // Microtask
console.log('5');                          // Sync

// Output: 1, 5, 3, 4, 2
```

---

### Q9. Prototypal Inheritance — How does it work?

```javascript
const animal = {
  eat() { console.log("Eating..."); }
};

const dog = Object.create(animal); // dog.__proto__ = animal
dog.bark = function() { console.log("Woof!"); };

dog.bark(); // "Woof!" — found on dog
dog.eat();  // "Eating..." — found on dog.__proto__ (animal)

// The chain: dog → animal → Object.prototype → null
```

**Interview follow-up:** "What's the difference between `__proto__` and `prototype`?"
- `__proto__` is the actual link in the chain (exists on every object)
- `prototype` is a property on **constructor functions** that becomes the `__proto__` of instances

---

### Q10. Explain `call()`, `apply()`, and `bind()`.

```javascript
function introduce(greeting, punctuation) {
  console.log(`${greeting}, I'm ${this.name}${punctuation}`);
}

const user = { name: "Nishant" };

// call — pass args individually
introduce.call(user, "Hello", "!");     // "Hello, I'm Nishant!"

// apply — pass args as array
introduce.apply(user, ["Hi", "."]);     // "Hi, I'm Nishant."

// bind — returns NEW function (doesn't execute)
const boundFn = introduce.bind(user, "Hey");
boundFn("?");                           // "Hey, I'm Nishant?"
```

---

## 📂 Category 2: Functions & Scope

### Q11. What is the difference between function declaration and expression?

```javascript
// Declaration — fully hoisted
sayHi();  // ✅ Works
function sayHi() { console.log("Hi"); }

// Expression — NOT fully hoisted
sayBye(); // ❌ TypeError: sayBye is not a function
var sayBye = function() { console.log("Bye"); };

// Named Function Expression — useful for recursion & stack traces
const factorial = function fact(n) {
  return n <= 1 ? 1 : n * fact(n - 1);
};
```

---

### Q12. What are Higher-Order Functions?

A function that **takes a function as argument** OR **returns a function**.

```javascript
// Takes function as argument
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(n => n * 2);     // [2, 4, 6, 8, 10]
const evens = numbers.filter(n => n % 2 === 0); // [2, 4]
const sum = numbers.reduce((acc, n) => acc + n, 0); // 15

// Returns a function
function multiplier(factor) {
  return (number) => number * factor;
}
const double = multiplier(2);
double(5); // 10
```

---

### Q13. What is Currying?

Transforming a function with multiple arguments into a sequence of functions each taking a single argument.

```javascript
// Normal
function add(a, b, c) { return a + b + c; }
add(1, 2, 3); // 6

// Curried
function curriedAdd(a) {
  return function(b) {
    return function(c) {
      return a + b + c;
    };
  };
}
curriedAdd(1)(2)(3); // 6

// Generic curry utility
function curry(fn) {
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    return (...nextArgs) => curried(...args, ...nextArgs);
  };
}

const curriedSum = curry(add);
curriedSum(1)(2)(3);   // 6
curriedSum(1, 2)(3);   // 6
curriedSum(1)(2, 3);   // 6
```

---

### Q14. What is an IIFE (Immediately Invoked Function Expression)?

```javascript
(function() {
  var secret = "hidden";
  console.log("IIFE runs immediately!");
})();

// console.log(secret); // ❌ ReferenceError — private!

// Modern use: async IIFE
(async () => {
  const data = await fetch('/api/data');
  console.log(await data.json());
})();
```

**Why it matters:** Before ES6 modules, IIFEs were the only way to create private scope and avoid global pollution.

---

### Q15. Explain `arguments` object vs rest parameters.

```javascript
// arguments — array-LIKE (no array methods)
function oldWay() {
  console.log(arguments);        // { 0: 'a', 1: 'b', length: 2 }
  console.log(arguments.map);    // undefined! Not a real array
  // Convert: Array.from(arguments) or [...arguments]
}

// Rest parameters — real array ✅
function newWay(...args) {
  console.log(args);             // ['a', 'b'] — real array
  console.log(args.map(x => x.toUpperCase())); // ['A', 'B']
}
```

**Note:** Arrow functions do NOT have their own `arguments` object.

---

## 📂 Category 3: Objects & Arrays

### Q16. Shallow Copy vs Deep Copy

```javascript
const original = { name: "Nishant", address: { city: "Delhi" } };

// Shallow Copy — nested objects are SHARED
const shallow = { ...original };
shallow.address.city = "Mumbai";
console.log(original.address.city); // "Mumbai" ← CHANGED!

// Deep Copy Methods
// 1. structuredClone (modern, best)
const deep1 = structuredClone(original);

// 2. JSON trick (fails with functions, Dates, undefined, circular refs)
const deep2 = JSON.parse(JSON.stringify(original));

// 3. Custom recursive (see 03_Coding_Problems.md)
```

---

### Q17. Object destructuring — Advanced patterns

```javascript
// Basic
const { name, age } = { name: "Nishant", age: 25 };

// Rename
const { name: userName } = { name: "Nishant" };

// Default values
const { role = "user" } = {};

// Nested
const { address: { city } } = { address: { city: "Delhi" } };

// Rest
const { id, ...rest } = { id: 1, name: "N", age: 25 };
// rest = { name: "N", age: 25 }

// Function parameters
function createUser({ name, age = 18, role = "user" } = {}) {
  return { name, age, role };
}
```

---

### Q18. Array methods you MUST know

```javascript
const arr = [1, 2, 3, 4, 5];

// map — transform each element (returns new array)
arr.map(x => x * 2);          // [2, 4, 6, 8, 10]

// filter — keep elements that pass test
arr.filter(x => x > 3);       // [4, 5]

// reduce — accumulate into single value
arr.reduce((sum, x) => sum + x, 0); // 15

// find — first match
arr.find(x => x > 3);         // 4

// findIndex — index of first match
arr.findIndex(x => x > 3);    // 3

// some — at least one passes?
arr.some(x => x > 4);         // true

// every — all pass?
arr.every(x => x > 0);        // true

// flat — flatten nested arrays
[1, [2, [3]]].flat(Infinity); // [1, 2, 3]

// flatMap — map + flat(1)
arr.flatMap(x => [x, x * 2]); // [1,2, 2,4, 3,6, 4,8, 5,10]

// at — negative indexing
arr.at(-1);                    // 5
```

---

### Q19. `Map` vs `Object` — When to use which?

| Feature | `Object` | `Map` |
| :--- | :--- | :--- |
| Key types | Strings/Symbols only | **Any type** (objects, functions) |
| Order | Not guaranteed (mostly) | **Insertion order guaranteed** |
| Size | `Object.keys(obj).length` | `map.size` (O(1)) |
| Iteration | `for...in` (includes prototype) | `for...of` (direct) |
| Performance | Slower for frequent add/delete | **Faster** for frequent add/delete |
| Serialization | `JSON.stringify` works | Need manual conversion |

```javascript
const map = new Map();
map.set({ id: 1 }, "user1");    // Object as key!
map.set(42, "answer");          // Number as key!
map.size;                       // 2
```

---

### Q20. `Set` and its practical uses

```javascript
// Remove duplicates
const arr = [1, 2, 2, 3, 3, 4];
const unique = [...new Set(arr)]; // [1, 2, 3, 4]

// Set operations
const a = new Set([1, 2, 3]);
const b = new Set([2, 3, 4]);

// Union
const union = new Set([...a, ...b]);       // {1, 2, 3, 4}

// Intersection
const intersection = new Set([...a].filter(x => b.has(x))); // {2, 3}

// Difference
const diff = new Set([...a].filter(x => !b.has(x)));        // {1}
```

---

## 📂 Category 4: Async JavaScript (Most Asked!)

### Q21. Promises — States and chaining

```javascript
// Three states: PENDING → FULFILLED or REJECTED
const promise = new Promise((resolve, reject) => {
  // async operation
  setTimeout(() => resolve("Done!"), 1000);
});

// Chaining — each .then() returns a NEW promise
fetch('/api/user')
  .then(res => res.json())        // returns promise
  .then(user => fetch(`/api/posts/${user.id}`))
  .then(res => res.json())
  .catch(err => console.error(err)) // catches ANY error above
  .finally(() => console.log("Cleanup")); // always runs
```

---

### Q22. `async/await` — Error handling patterns

```javascript
// Pattern 1: try/catch
async function fetchUser() {
  try {
    const res = await fetch('/api/user');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error("Failed:", err.message);
    return null; // graceful fallback
  }
}

// Pattern 2: Wrapper function (no try/catch clutter)
function to(promise) {
  return promise
    .then(data => [null, data])
    .catch(err => [err, null]);
}

async function loadData() {
  const [err, user] = await to(fetch('/api/user'));
  if (err) return console.error(err);
  console.log(user);
}
```

---

### Q23. `Promise.all` vs `Promise.allSettled` vs `Promise.race` vs `Promise.any`

```javascript
const p1 = Promise.resolve(1);
const p2 = Promise.reject("Error");
const p3 = Promise.resolve(3);

// all — FAILS FAST if any rejects
Promise.all([p1, p2, p3]).catch(e => e);       // "Error"

// allSettled — waits for ALL, never rejects
Promise.allSettled([p1, p2, p3]);
// [{status:"fulfilled",value:1}, {status:"rejected",reason:"Error"}, ...]

// race — first to settle (resolve OR reject) wins
Promise.race([p1, p2, p3]);                   // 1

// any — first to RESOLVE wins (ignores rejections)
Promise.any([p2, p1, p3]);                    // 1
```

---

### Q24. What is callback hell and how to avoid it?

```javascript
// ❌ Callback Hell
getUser(userId, (user) => {
  getOrders(user.id, (orders) => {
    getOrderDetails(orders[0].id, (details) => {
      getShipping(details.shippingId, (shipping) => {
        console.log(shipping); // Deeply nested!
      });
    });
  });
});

// ✅ Fix with async/await
async function getShippingInfo(userId) {
  const user = await getUser(userId);
  const orders = await getOrders(user.id);
  const details = await getOrderDetails(orders[0].id);
  const shipping = await getShipping(details.shippingId);
  return shipping;
}
```

---

### Q25. Explain Event Delegation

```javascript
// ❌ Bad: Adding listener to every button
document.querySelectorAll('.btn').forEach(btn => {
  btn.addEventListener('click', handleClick);
});

// ✅ Good: One listener on parent (Event Delegation)
document.getElementById('button-container').addEventListener('click', (e) => {
  if (e.target.matches('.btn')) {
    handleClick(e);
  }
});
```

**Why?** Fewer listeners = less memory. Works for dynamically added elements too.

---

## 📂 Category 5: ES6+ Modern Features

### Q26. Spread vs Rest operator

```javascript
// Spread — expands elements
const arr1 = [1, 2];
const arr2 = [...arr1, 3, 4];      // [1, 2, 3, 4]
const obj1 = { a: 1 };
const obj2 = { ...obj1, b: 2 };    // { a: 1, b: 2 }

// Rest — collects elements
function sum(...numbers) {          // rest in params
  return numbers.reduce((a, b) => a + b, 0);
}
const { first, ...remaining } = { first: 1, second: 2, third: 3 };
// remaining = { second: 2, third: 3 }
```

---

### Q27. Template Literals & Tagged Templates

```javascript
// Basic
const name = "Nishant";
console.log(`Hello, ${name}!`);

// Multi-line
const html = `
  <div>
    <h1>${name}</h1>
  </div>
`;

// Tagged Templates (used in styled-components, GraphQL)
function highlight(strings, ...values) {
  return strings.reduce((result, str, i) => {
    return result + str + (values[i] ? `<mark>${values[i]}</mark>` : '');
  }, '');
}

const result = highlight`Hello ${name}, you have ${5} messages`;
// "Hello <mark>Nishant</mark>, you have <mark>5</mark> messages"
```

---

### Q28. Optional Chaining (`?.`) & Nullish Coalescing (`??`)

```javascript
const user = { address: { street: null } };

// Optional Chaining — safe property access
user?.address?.street?.name;    // undefined (no error!)
user?.getProfile?.();           // undefined (safe method call)
user?.orders?.[0];              // undefined (safe array access)

// Nullish Coalescing — default for null/undefined ONLY
const name = null ?? "Default";      // "Default"
const count = 0 ?? 42;              // 0 (0 is NOT nullish!)
const empty = "" ?? "fallback";     // "" (empty string is NOT nullish!)

// Compare with ||
const count2 = 0 || 42;             // 42 (|| treats 0 as falsy!)
```

---

### Q29. Generators and Iterators

```javascript
// Generator function
function* idGenerator() {
  let id = 1;
  while (true) {
    yield id++;
  }
}

const gen = idGenerator();
gen.next(); // { value: 1, done: false }
gen.next(); // { value: 2, done: false }

// Custom Iterable
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

for (const num of range) console.log(num); // 1, 2, 3, 4, 5
```

---

### Q30. `WeakMap` and `WeakRef` — When and Why?

```javascript
// WeakMap — keys are weakly held (GC can collect them)
const cache = new WeakMap();

function process(obj) {
  if (cache.has(obj)) return cache.get(obj);
  const result = /* expensive computation */ obj.value * 2;
  cache.set(obj, result);
  return result;
}

let data = { value: 42 };
process(data); // Cached
data = null;   // Object can be garbage collected! WeakMap doesn't prevent it.

// Use cases: storing metadata about DOM nodes, private data, memoization
```

---

## 📂 Category 6: DOM & Browser

### Q31. What is the Critical Rendering Path?

```
HTML → DOM Tree
                 → Render Tree → Layout → Paint → Composite
CSS  → CSSOM
```

1. **DOM** — Parse HTML into a tree of nodes
2. **CSSOM** — Parse CSS into a style tree
3. **Render Tree** — Combine DOM + CSSOM (skip `display:none`)
4. **Layout** — Calculate positions and sizes
5. **Paint** — Fill in pixels
6. **Composite** — Layer composition on GPU

---

### Q32. `localStorage` vs `sessionStorage` vs Cookies

| Feature | localStorage | sessionStorage | Cookies |
| :--- | :--- | :--- | :--- |
| Capacity | ~5-10 MB | ~5 MB | ~4 KB |
| Expiry | Never | Tab close | Configurable |
| Sent to server? | ❌ No | ❌ No | ✅ Every request |
| Scope | Origin | Origin + Tab | Origin + Path |

---

### Q33. Debouncing vs Throttling

```javascript
// Debounce — wait until user STOPS doing something
// Use: Search input, window resize
function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

// Throttle — execute at most once every N ms
// Use: Scroll handler, mousemove
function throttle(fn, limit) {
  let inThrottle = false;
  return (...args) => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}
```

---

## 📂 Category 7: Error Handling & Misc

### Q34. Error handling best practices

```javascript
// Custom Error classes
class ValidationError extends Error {
  constructor(field, message) {
    super(message);
    this.name = 'ValidationError';
    this.field = field;
  }
}

// Global error handlers
window.addEventListener('error', (e) => {
  console.error('Uncaught:', e.error);
});

window.addEventListener('unhandledrejection', (e) => {
  console.error('Unhandled Promise:', e.reason);
  e.preventDefault(); // Prevent default logging
});
```

---

### Q35. What is `"use strict"`?

Strict mode catches common coding mistakes:
- Cannot use undeclared variables
- Cannot delete variables/functions
- Cannot use duplicate parameter names
- `this` is `undefined` in functions (not `window`)
- Disallows `with` statement
- Prevents assigning to read-only properties

```javascript
"use strict";
x = 10;            // ❌ ReferenceError
delete Object.prototype; // ❌ TypeError
function f(a, a) {} // ❌ SyntaxError
```

---

### Q36–Q50: Rapid Fire Questions

| # | Question | Answer |
| :--- | :--- | :--- |
| 36 | What is `typeof` operator? | Returns string type: `"string"`, `"number"`, `"boolean"`, `"object"`, `"function"`, `"undefined"`, `"symbol"`, `"bigint"` |
| 37 | What is `instanceof`? | Checks prototype chain: `[] instanceof Array // true` |
| 38 | What are Pure Functions? | Same input → same output, no side effects |
| 39 | What is Memoization? | Cache function results based on inputs |
| 40 | What is Event Bubbling? | Events propagate from target UP to root |
| 41 | What is Event Capturing? | Events propagate from root DOWN to target |
| 42 | `stopPropagation` vs `preventDefault`? | Stop bubble/capture vs prevent default behavior |
| 43 | What is `Object.freeze()` vs `Object.seal()`? | freeze = no add/modify/delete; seal = no add/delete but CAN modify |
| 44 | What is a Proxy? | Intercept/customize object operations (get, set, delete) |
| 45 | What is `Symbol`? | Unique identifier, used for private properties & well-known protocols |
| 46 | What is tree shaking? | Remove unused exports during bundling |
| 47 | What is a Service Worker? | Background script for offline caching, push notifications |
| 48 | `for...in` vs `for...of`? | `in` = keys/indexes (objects); `of` = values (iterables) |
| 49 | What is `Object.create()`? | Creates object with specified prototype |
| 50 | What is `globalThis`? | Universal reference to global object (works in browser, Node, workers) |

---

## 💡 Interview Pro Tips

1. **Always ask clarifying questions** before answering
2. **Think out loud** — explain your reasoning process
3. **Mention trade-offs** — there's rarely one "right" answer
4. **Know the "why"** — not just what, but why it exists
5. **Relate to real projects** — "In my last project, I used this when..."

---

## 🔗 Navigation

**Prev:** [04_Machine_Coding_JS.md](04_Machine_Coding_JS.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [06_Async_Interview_Mastery.md](06_Async_Interview_Mastery.md)
