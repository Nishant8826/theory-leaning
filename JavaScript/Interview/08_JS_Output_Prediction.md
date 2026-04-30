# 📌 08 — JavaScript Output Prediction (Most Popular Interview Format)

## 🌟 Introduction

**"What is the output?"** is the #1 most common JavaScript interview question format. These questions test your deep understanding of execution context, closures, hoisting, coercion, and async behavior. **Practice these until you can answer without thinking.**

---

## 📂 Section 1: Hoisting & Scope

### Problem 1
```javascript
var a = 1;
function foo() {
  console.log(a);
  var a = 2;
  console.log(a);
}
foo();
```
<details>
<summary>🔍 Answer</summary>

```
undefined
2
```
**Why?** The local `var a` is hoisted inside `foo()`, shadowing the global `a`. At the first `console.log`, local `a` exists but hasn't been assigned yet → `undefined`.
</details>

---

### Problem 2
```javascript
console.log(x);
console.log(y);
var x = 1;
let y = 2;
```
<details>
<summary>🔍 Answer</summary>

```
undefined
ReferenceError: Cannot access 'y' before initialization
```
**Why?** `var x` is hoisted and initialized to `undefined`. `let y` is hoisted but stays in the **Temporal Dead Zone (TDZ)** until its declaration.
</details>

---

### Problem 3
```javascript
function test() {
  console.log(a);
  console.log(foo());

  var a = 1;
  function foo() {
    return 2;
  }
}
test();
```
<details>
<summary>🔍 Answer</summary>

```
undefined
2
```
**Why?** `var a` hoists as `undefined`. Function declarations are **fully hoisted** (name + body), so `foo()` works even before its definition.
</details>

---

## 📂 Section 2: Closures

### Problem 4
```javascript
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 0);
}
```
<details>
<summary>🔍 Answer</summary>

```
3
3
3
```
**Why?** `var` has function scope. There's only ONE `i`, and by the time `setTimeout` runs, the loop is done and `i === 3`.

**Fix with `let`:**
```javascript
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 0);
}
// Output: 0, 1, 2 (let creates new binding per iteration)
```
</details>

---

### Problem 5
```javascript
function createFunctions() {
  const result = [];
  for (var i = 0; i < 5; i++) {
    result.push(function() { return i; });
  }
  return result;
}

const funcs = createFunctions();
console.log(funcs[0]());
console.log(funcs[2]());
console.log(funcs[4]());
```
<details>
<summary>🔍 Answer</summary>

```
5
5
5
```
**Why?** Same closure over single `var i`. All functions share the same `i`, which is `5` after the loop. Fix: use `let` or an IIFE.
</details>

---

### Problem 6
```javascript
function outer() {
  let count = 0;
  return {
    increment: () => ++count,
    getCount: () => count,
  };
}

const counter1 = outer();
const counter2 = outer();

counter1.increment();
counter1.increment();
counter2.increment();

console.log(counter1.getCount());
console.log(counter2.getCount());
```
<details>
<summary>🔍 Answer</summary>

```
2
1
```
**Why?** Each call to `outer()` creates a **new closure** with its own `count`. They don't share state.
</details>

---

## 📂 Section 3: `this` Keyword

### Problem 7
```javascript
const obj = {
  name: 'Nishant',
  greet: function() {
    console.log(this.name);
  },
  greetArrow: () => {
    console.log(this.name);
  }
};

obj.greet();
obj.greetArrow();
```
<details>
<summary>🔍 Answer</summary>

```
Nishant
undefined
```
**Why?** Regular function: `this` = calling object (`obj`). Arrow function: `this` = lexical scope (global/module), NOT `obj`.
</details>

---

### Problem 8
```javascript
const obj = {
  name: 'Nishant',
  greet() {
    return function() {
      console.log(this.name);
    };
  }
};

obj.greet()();
```
<details>
<summary>🔍 Answer</summary>

```
undefined
```
**Why?** `obj.greet()` returns a function. When that function is called as `()()`, it's a standalone call — `this` = `window` (non-strict) which may not have `.name`. **Fix:** use an arrow function inside, or `.bind(this)`.
</details>

---

### Problem 9
```javascript
function Person(name) {
  this.name = name;
  this.sayHi = () => {
    console.log(this.name);
  };
}

const p = new Person('Nishant');
const fn = p.sayHi;
fn();
```
<details>
<summary>🔍 Answer</summary>

```
Nishant
```
**Why?** Arrow functions capture `this` from their **creation context**. `this` was `p` when the arrow function was created (inside the `new` call). Even when extracted, `this` stays bound to `p`.
</details>

---

## 📂 Section 4: Event Loop & Async

### Problem 10
```javascript
console.log('1');
setTimeout(() => console.log('2'), 0);
Promise.resolve().then(() => console.log('3'));
setTimeout(() => console.log('4'), 0);
Promise.resolve().then(() => console.log('5'));
console.log('6');
```
<details>
<summary>🔍 Answer</summary>

```
1
6
3
5
2
4
```
**Why?** Sync first (1, 6) → Microtasks (3, 5) → Macrotasks (2, 4).
</details>

---

### Problem 11
```javascript
async function foo() {
  console.log('A');
  await Promise.resolve();
  console.log('B');
}

console.log('C');
foo();
console.log('D');
```
<details>
<summary>🔍 Answer</summary>

```
C
A
D
B
```
**Why?** `C` (sync) → `foo()` starts → `A` (sync inside foo) → `await` pauses foo → `D` (sync) → `B` (microtask from await).
</details>

---

### Problem 12
```javascript
setTimeout(() => console.log('timeout'), 0);

Promise.resolve()
  .then(() => {
    console.log('promise 1');
    return Promise.resolve();
  })
  .then(() => console.log('promise 2'));

queueMicrotask(() => console.log('microtask'));
console.log('sync');
```
<details>
<summary>🔍 Answer</summary>

```
sync
promise 1
microtask
promise 2
timeout
```
**Why?** Sync → microtask queue drains: `promise 1` runs (queues `promise 2`), `microtask` runs → `promise 2` runs → macrotask: `timeout`.
</details>

---

## 📂 Section 5: Coercion & Equality

### Problem 13
```javascript
console.log([] == false);
console.log([] == ![]);
console.log('' == false);
console.log(null == false);
console.log(undefined == false);
```
<details>
<summary>🔍 Answer</summary>

```
true
true
true
false
false
```
**Why?**
- `[] == false` → `"" == 0` → `0 == 0` → `true`
- `[] == ![]` → `[] == false` → same as above → `true`
- `'' == false` → `0 == 0` → `true`
- `null == false` → `false` (null only equals undefined)
- `undefined == false` → `false` (undefined only equals null)
</details>

---

### Problem 14
```javascript
console.log(1 + '2' + 3);
console.log(1 + 2 + '3');
console.log('1' - 2 + 3);
console.log('10' - '4' - '2');
console.log(3 > 2 > 1);
```
<details>
<summary>🔍 Answer</summary>

```
"123"
"33"
2
4
false
```
**Why?**
- `1 + '2'` = `"12"`, then `"12" + 3` = `"123"`
- `1 + 2` = `3`, then `3 + '3'` = `"33"`
- `'1' - 2` = `-1`, then `-1 + 3` = `2`
- `'10' - '4'` = `6`, then `6 - '2'` = `4`
- `3 > 2` = `true`, then `true > 1` = `1 > 1` = `false`
</details>

---

## 📂 Section 6: Prototype & Object

### Problem 15
```javascript
function Dog(name) {
  this.name = name;
}
Dog.prototype.bark = function() {
  console.log(this.name + ' says woof');
};

const d1 = new Dog('Rex');
const d2 = new Dog('Max');

d1.bark();
console.log(d1.bark === d2.bark);
console.log(d1.hasOwnProperty('name'));
console.log(d1.hasOwnProperty('bark'));
```
<details>
<summary>🔍 Answer</summary>

```
Rex says woof
true
true
false
```
**Why?** `bark` is on the prototype (shared), not on the instance. `name` is on each instance. `hasOwnProperty` only checks own properties.
</details>

---

### Problem 16
```javascript
const a = {};
const b = { key: 'b' };
const c = { key: 'c' };

a[b] = 123;
a[c] = 456;

console.log(a[b]);
```
<details>
<summary>🔍 Answer</summary>

```
456
```
**Why?** Object keys must be strings. Both `b` and `c` convert to `"[object Object]"`. So `a["[object Object]"]` is overwritten to `456`.
</details>

---

## 📂 Section 7: Miscellaneous Tricky

### Problem 17
```javascript
const arr = [1, 2, 3];
arr[10] = 11;
console.log(arr.length);
console.log(arr.filter(x => x === undefined).length);
```
<details>
<summary>🔍 Answer</summary>

```
11
0
```
**Why?** Setting `arr[10]` creates a **sparse array** with length 11. Indices 3-9 are "empty slots" (not `undefined`). Array methods skip empty slots.
</details>

---

### Problem 18
```javascript
console.log(typeof typeof 1);
```
<details>
<summary>🔍 Answer</summary>

```
"string"
```
**Why?** `typeof 1` = `"number"` (a string). `typeof "number"` = `"string"`.
</details>

---

### Problem 19
```javascript
const a = [1, 2, 3];
const b = [1, 2, 3];
const c = a;

console.log(a == b);
console.log(a === b);
console.log(a == c);
```
<details>
<summary>🔍 Answer</summary>

```
false
false
true
```
**Why?** Arrays are objects. `==` and `===` compare **references**, not values. `a` and `b` are different objects. `c` points to the same object as `a`.
</details>

---

### Problem 20
```javascript
console.log(0.1 + 0.2 === 0.3);
console.log(0.1 + 0.2);
console.log(Number((0.1 + 0.2).toFixed(1)) === 0.3);
```
<details>
<summary>🔍 Answer</summary>

```
false
0.30000000000000004
true
```
**Why?** IEEE 754 floating-point precision. Use `toFixed()` or epsilon comparison: `Math.abs(a - b) < Number.EPSILON`.
</details>

---

## 💡 Cheat Sheet: Output Prediction Strategy

| See This... | Think About... |
| :--- | :--- |
| `var` in a loop | Shared variable, closure trap |
| `setTimeout(..., 0)` | Macrotask — runs LAST |
| `.then()` | Microtask — runs before macrotasks |
| `await` | Pauses function, rest becomes microtask |
| Arrow function | No own `this`, inherits from outer scope |
| `+` with mixed types | String wins (concatenation) |
| `-` with strings | Number wins (subtraction) |
| `== ` (loose) | Type coercion happens |
| Object as key | Converts to `"[object Object]"` |
| Array comparison | Reference equality, not value |

---

## 🔗 Navigation

**Prev:** [07_Realtime_Scenario_Problems.md](07_Realtime_Scenario_Problems.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [09_ES6_Plus_Interview.md](09_ES6_Plus_Interview.md)
