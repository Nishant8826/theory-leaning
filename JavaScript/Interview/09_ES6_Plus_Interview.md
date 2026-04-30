# 📌 09 — ES6+ Features Interview Questions

## 🌟 Introduction

Modern JavaScript interviews **expect ES6+ fluency**. You'll be asked to explain features, compare old vs new approaches, and solve problems using modern syntax. This file covers every ES6+ feature that interviewers care about.

---

## 🏗️ 1. Arrow Functions — Deep Dive

### Q: What are the differences between arrow functions and regular functions?

| Feature | Regular Function | Arrow Function |
| :--- | :--- | :--- |
| `this` binding | Dynamic (call-time) | Lexical (definition-time) |
| `arguments` object | ✅ Has own | ❌ Inherits from outer |
| Can be constructor | ✅ `new Person()` | ❌ Throws TypeError |
| `prototype` property | ✅ Has one | ❌ No prototype |
| Method definition | ✅ Appropriate | ❌ Avoid (wrong `this`) |
| Callbacks | ✅ Works | ✅ Preferred (concise) |

```javascript
// When NOT to use arrow functions:
const obj = {
  value: 42,
  getValue: () => this.value, // ❌ this = global, not obj
};

// When TO use arrow functions:
class Timer {
  constructor() {
    this.seconds = 0;
    setInterval(() => this.seconds++, 1000); // ✅ this = Timer instance
  }
}
```

---

## 🏗️ 2. Destructuring — Advanced Patterns

```javascript
// Swap variables
let a = 1, b = 2;
[a, b] = [b, a]; // a=2, b=1

// Ignore values
const [first, , third] = [1, 2, 3]; // first=1, third=3

// Dynamic key destructuring
const key = 'name';
const { [key]: value } = { name: 'Nishant' }; // value = 'Nishant'

// Nested with defaults
const {
  user: { name = 'Anonymous', age = 0 } = {}
} = { user: { name: 'Nishant' } };
// name = 'Nishant', age = 0

// Function parameter destructuring with validation
function createUser({ name, email, role = 'user' } = {}) {
  if (!name || !email) throw new Error('name and email required');
  return { name, email, role, createdAt: new Date() };
}
```

---

## 🏗️ 3. Spread & Rest — Interview Questions

### Q: What's the output?

```javascript
const arr1 = [1, 2, 3];
const arr2 = [...arr1];
arr2.push(4);

console.log(arr1); // [1, 2, 3] — unaffected (shallow copy)
console.log(arr2); // [1, 2, 3, 4]

// Merge objects (last one wins)
const defaults = { theme: 'dark', lang: 'en', debug: false };
const userPrefs = { theme: 'light', debug: true };
const config = { ...defaults, ...userPrefs };
// { theme: 'light', lang: 'en', debug: true }
```

### Q: Spread creates a shallow copy, not deep. Prove it.

```javascript
const original = { a: 1, nested: { b: 2 } };
const copy = { ...original };
copy.nested.b = 99;

console.log(original.nested.b); // 99 ← CHANGED! (same reference)
```

---

## 🏗️ 4. `class` Syntax — What You Must Know

```javascript
class Animal {
  // Private field (ES2022)
  #sound;

  // Static property
  static kingdom = 'Animalia';

  constructor(name, sound) {
    this.name = name;
    this.#sound = sound;
  }

  // Getter
  get info() {
    return `${this.name} says ${this.#sound}`;
  }

  // Static method
  static create(name, sound) {
    return new Animal(name, sound);
  }

  // Instance method
  speak() {
    console.log(this.#sound);
  }
}

class Dog extends Animal {
  constructor(name) {
    super(name, 'Woof'); // Must call super() first
  }

  fetch(item) {
    console.log(`${this.name} fetches ${item}`);
  }
}

const dog = new Dog('Rex');
dog.speak();   // "Woof"
dog.info;      // "Rex says Woof"
Dog.kingdom;   // "Animalia" (inherited static)
```

### Q: Is JS class "real" OOP?

**No.** JavaScript classes are **syntactic sugar** over prototypal inheritance. Under the hood, it still uses `[[Prototype]]` chain. There's no true class-based inheritance like Java/C++.

---

## 🏗️ 5. Modules — `import` / `export`

```javascript
// Named exports
export const PI = 3.14;
export function add(a, b) { return a + b; }

// Default export (one per file)
export default class Calculator { /* ... */ }

// Import
import Calculator, { PI, add } from './math.js';
import * as MathUtils from './math.js';

// Dynamic import (code splitting)
const module = await import('./heavy-module.js');
module.doSomething();
```

### Q: What's the difference between CommonJS and ES Modules?

| Feature | CommonJS (`require`) | ES Modules (`import`) |
| :--- | :--- | :--- |
| Loading | Synchronous | Asynchronous |
| Binding | Copy of value | **Live binding** (reference) |
| When parsed | Runtime | Compile time (static) |
| Tree-shaking | ❌ Difficult | ✅ Supported |
| Top-level await | ❌ No | ✅ Yes |
| `this` at top | `module.exports` | `undefined` |

---

## 🏗️ 6. Promises — Advanced Patterns

### Promise.withResolvers() (ES2024)

```javascript
// Old way
let resolve, reject;
const promise = new Promise((res, rej) => {
  resolve = res;
  reject = rej;
});

// New way (ES2024)
const { promise, resolve, reject } = Promise.withResolvers();
```

### Convert callback to Promise

```javascript
function readFilePromise(path) {
  return new Promise((resolve, reject) => {
    fs.readFile(path, 'utf8', (err, data) => {
      if (err) reject(err);
      else resolve(data);
    });
  });
}

// Or use util.promisify (Node.js)
const { promisify } = require('util');
const readFile = promisify(fs.readFile);
```

---

## 🏗️ 7. New Data Structures

### Map — Ordered key-value pairs

```javascript
const map = new Map();
map.set('a', 1);
map.set({ id: 1 }, 'obj key');
map.set(42, 'number key');

// Iteration
for (const [key, value] of map) {
  console.log(key, value);
}

// Convert to/from Object
const obj = Object.fromEntries(map);
const map2 = new Map(Object.entries(obj));
```

### WeakMap — Keys must be objects, GC-friendly

```javascript
const metadata = new WeakMap();
let element = document.querySelector('#btn');
metadata.set(element, { clicks: 0 });

// When element is removed from DOM and reference is lost,
// the WeakMap entry is automatically garbage collected
element = null; // GC can now clean up both element AND metadata
```

### Set — Unique values only

```javascript
// Deduplicate with type preservation
const set = new Set([1, '1', 1, 2, 2, 3]);
console.log([...set]); // [1, '1', 2, 3]

// Set has O(1) lookup
set.has(2); // true — faster than array.includes()
```

---

## 🏗️ 8. Iterators & Generators

### Custom Iterator Protocol

```javascript
// Any object with [Symbol.iterator]() is iterable
const fibonacci = {
  [Symbol.iterator]() {
    let [prev, curr] = [0, 1];
    return {
      next() {
        [prev, curr] = [curr, prev + curr];
        return { value: prev, done: false };
      }
    };
  }
};

// Works with for...of, spread, destructuring
const [f1, f2, f3, f4, f5] = fibonacci;
console.log(f1, f2, f3, f4, f5); // 1, 1, 2, 3, 5
```

### Generator — Pausable Functions

```javascript
function* idMaker() {
  let id = 0;
  while (true) {
    const reset = yield id++;
    if (reset) id = 0;
  }
}

const gen = idMaker();
gen.next();        // { value: 0, done: false }
gen.next();        // { value: 1, done: false }
gen.next(true);    // { value: 0, done: false } — reset!
gen.next();        // { value: 1, done: false }
```

### Async Generator — Streaming Data

```javascript
async function* streamLogs(url) {
  const response = await fetch(url);
  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    yield decoder.decode(value);
  }
}

for await (const chunk of streamLogs('/api/logs')) {
  console.log(chunk);
}
```

---

## 🏗️ 9. Proxy & Reflect

```javascript
// Validation Proxy
function createValidatedObject(validations) {
  return new Proxy({}, {
    set(target, prop, value) {
      const validate = validations[prop];
      if (validate && !validate(value)) {
        throw new TypeError(`Invalid value for ${prop}: ${value}`);
      }
      return Reflect.set(target, prop, value);
    },
    get(target, prop) {
      if (!(prop in target)) {
        throw new ReferenceError(`Property ${prop} does not exist`);
      }
      return Reflect.get(target, prop);
    }
  });
}

const user = createValidatedObject({
  age: (v) => typeof v === 'number' && v >= 0 && v <= 150,
  email: (v) => typeof v === 'string' && v.includes('@'),
});

user.age = 25;       // ✅ OK
user.email = 'test'; // ❌ TypeError: Invalid value for email
```

### Real-world Proxy use cases:
- **Reactive frameworks** (Vue 3 uses Proxy for reactivity)
- **API mocking** (intercept property access)
- **Logging/debugging** (log every get/set)
- **Default values** (return defaults for missing props)
- **Access control** (restrict certain operations)

---

## 🏗️ 10. Modern Syntax Sugar

### Object shorthand

```javascript
const name = 'Nishant';
const age = 25;

// Shorthand properties
const user = { name, age }; // Same as { name: name, age: age }

// Computed property names
const key = 'role';
const obj = { [key]: 'admin', [`${key}Id`]: 42 };
// { role: 'admin', roleId: 42 }

// Shorthand methods
const api = {
  getData() { /* ... */ },          // Instead of getData: function() {}
  async fetchUser() { /* ... */ },  // Async shorthand
};
```

### Logical Assignment Operators (ES2021)

```javascript
// ||= (assign if falsy)
let x = 0;
x ||= 10;   // x = 10 (0 is falsy)

// &&= (assign if truthy)
let y = 1;
y &&= 20;   // y = 20 (1 is truthy)

// ??= (assign if nullish — null/undefined only)
let z = 0;
z ??= 10;   // z = 0 (0 is NOT nullish!)

let w = null;
w ??= 10;   // w = 10 (null IS nullish)
```

### Array.at() & Object.hasOwn() (ES2022)

```javascript
const arr = [1, 2, 3, 4, 5];
arr.at(-1);   // 5 (last element)
arr.at(-2);   // 4

// Object.hasOwn — safer than hasOwnProperty
const obj = Object.create(null); // No prototype!
obj.key = 'value';
// obj.hasOwnProperty('key'); // ❌ TypeError
Object.hasOwn(obj, 'key');     // ✅ true
```

### structuredClone() (ES2022)

```javascript
const original = {
  date: new Date(),
  set: new Set([1, 2, 3]),
  nested: { deep: true },
};

const clone = structuredClone(original);
clone.nested.deep = false;

console.log(original.nested.deep); // true (deep copy!)
console.log(clone.date instanceof Date); // true (preserves types!)
```

---

## 📐 ES6+ Feature Timeline

| Year | Key Features |
| :--- | :--- |
| ES2015 (ES6) | `let/const`, arrow functions, classes, promises, template literals, destructuring, modules, `Map/Set`, `Symbol`, generators |
| ES2016 | `Array.includes()`, `**` exponentiation |
| ES2017 | `async/await`, `Object.entries/values`, string padding |
| ES2018 | Rest/spread for objects, `for await...of`, `Promise.finally` |
| ES2019 | `Array.flat/flatMap`, `Object.fromEntries`, optional catch binding |
| ES2020 | Optional chaining `?.`, nullish coalescing `??`, `BigInt`, `Promise.allSettled`, `globalThis` |
| ES2021 | Logical assignment `||= &&= ??=`, `String.replaceAll`, numeric separators `1_000_000` |
| ES2022 | Top-level await, `Array.at()`, private fields `#`, `Object.hasOwn`, `structuredClone` |
| ES2023 | `Array.findLast/findLastIndex`, hashbang grammar |
| ES2024 | `Promise.withResolvers`, `Object.groupBy`, `Map.groupBy` |

---

## 🔗 Navigation

**Prev:** [08_JS_Output_Prediction.md](08_JS_Output_Prediction.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [10_DSA_In_JavaScript.md](10_DSA_In_JavaScript.md)
