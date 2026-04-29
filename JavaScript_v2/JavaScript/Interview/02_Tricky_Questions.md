# 📌 02 — Tricky JavaScript Questions

## 🧠 Overview

These questions are designed to catch off-guard even experienced developers. They probe for understanding of coercion, scoping, timing, and reference semantics.

---

## Question Set 1 — Execution Order

### Q1: What is the output?

```javascript
console.log('1')
setTimeout(() => console.log('2'), 0)
Promise.resolve().then(() => console.log('3'))
console.log('4')
```

**Answer: 1, 4, 3, 2**

1 and 4 are synchronous. 3 is a microtask (runs before next task). 2 is a macrotask (setTimeout).

---

### Q2: What is the output?

```javascript
let x = 1
const fn = () => {
  console.log(x)
  let x = 2
}
fn()
```

**Answer: ReferenceError (Temporal Dead Zone)**

`let x = 2` inside `fn` is hoisted to the top of `fn`'s scope but not initialized. Reading `x` before the `let x = 2` line throws TDZ ReferenceError.

---

### Q3: What is the output?

```javascript
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 0)
}
```

**Answer: 3, 3, 3**

`var` is function-scoped. All three callbacks share the same `i` variable. By the time setTimeout fires (next task), the loop has completed and `i === 3`.

Fix with `let` (block-scoped) or closure: `setTimeout(((i) => () => console.log(i))(i), 0)`.

---

### Q4: What is the output?

```javascript
console.log(typeof undefined)  // 'undefined'
console.log(typeof null)       // 'object'
console.log(typeof NaN)        // 'number'
console.log(typeof function(){}) // 'function'
console.log(typeof class {})    // 'function'
console.log(typeof Symbol())    // 'symbol'
console.log(typeof 42n)         // 'bigint'
console.log(typeof [])          // 'object'
```

---

## Question Set 2 — Coercion Traps

### Q5: What does this evaluate to?

```javascript
[] + []   // ''
[] + {}   // '[object Object]'
{} + []   // 0 (block + unary plus on array)
{} + {}   // NaN (block + unary plus on object)
true + true  // 2
'5' - 3   // 2 (subtraction coerces string to number)
'5' + 3   // '53' (addition coerces to string)
```

**Key rule:** `+` is concatenation if EITHER operand is a string (or object that converts to string). `-` always coerces to number.

---

### Q6: Explain `[] == ![]`

```javascript
[] == ![]  // true
```

Step by step:
1. `![]` → `false` ([] is truthy, !truthy = false)
2. Now: `[] == false`
3. `false` is boolean → convert to number: `0`
4. Now: `[] == 0`
5. `[]` is object → ToPrimitive: `[].toString()` → `""` → `Number("") = 0`
6. Now: `0 == 0` → `true`

---

## Question Set 3 — Closures and Scope

### Q7: Fix the classic closure bug

```javascript
// Broken:
const funcs = []
for (var i = 0; i < 5; i++) {
  funcs.push(function() { return i })
}
funcs[0]()  // Returns 5, not 0

// Fix 1: let
for (let i = 0; i < 5; i++) {
  funcs.push(function() { return i })  // Each i is block-scoped
}

// Fix 2: IIFE
for (var i = 0; i < 5; i++) {
  funcs.push((function(i) { return function() { return i } })(i))
}

// Fix 3: .bind
for (var i = 0; i < 5; i++) {
  funcs.push(function(i) { return i }.bind(null, i))
}
```

---

### Q8: What does this output and why?

```javascript
function createCounter() {
  let count = 0
  return {
    increment: () => ++count,
    decrement: () => --count,
    value: () => count,
    reset: () => { count = 0 }
  }
}

const counter = createCounter()
counter.increment()
counter.increment()
counter.increment()
counter.decrement()
console.log(counter.value())  // 2
```

Answer: 2. All methods share the same `count` via closure over createCounter's context.

---

## Question Set 4 — Prototype Tricks

### Q9: What is the output?

```javascript
function Foo() {}
Foo.prototype.x = 1

const a = new Foo()
const b = new Foo()

a.x = 2  // Own property on a
console.log(a.x)  // 2 (own property)
console.log(b.x)  // 1 (from prototype — b has no own 'x')

delete a.x  // Delete own property
console.log(a.x)  // 1 (now falls through to prototype)

Foo.prototype.x = 99
console.log(b.x)  // 99 (prototype updated)
console.log(a.x)  // 99 (a now reads from prototype again)
```

---

### Q10: Inheritance vs Prototype Chain

```javascript
class Animal {
  constructor(name) { this.name = name }
  speak() { return `${this.name} makes a sound` }
}

class Dog extends Animal {
  speak() { return `${super.speak()} (woof!)` }
}

const d = new Dog('Rex')
console.log(d.speak())  // 'Rex makes a sound (woof!)'

// Prototype chain:
Object.getPrototypeOf(d) === Dog.prototype  // true
Object.getPrototypeOf(Dog.prototype) === Animal.prototype  // true
Object.getPrototypeOf(Animal.prototype) === Object.prototype  // true
Object.getPrototypeOf(Object.prototype) === null  // true

d instanceof Dog     // true
d instanceof Animal  // true
d instanceof Object  // true
```

---

## Question Set 5 — Async Traps

### Q11: What is the output?

```javascript
async function foo() {
  console.log('1')
  await Promise.resolve()
  console.log('2')
}

console.log('3')
foo()
console.log('4')
```

**Answer: 3, 1, 4, 2**

- 3: sync
- foo() called: '1' (sync inside foo)
- await suspends foo: returns to outer code
- '4': sync (outer)
- Microtask: foo resumes → '2'

---

### Q12: Identify the bug

```javascript
async function processItems(items) {
  items.forEach(async (item) => {
    await processItem(item)  // Bug!
  })
  console.log('All processed!')
}
```

**Bug:** `forEach` doesn't await async callbacks. `processItems` completes immediately after starting all forEach iterations. "All processed!" logs before ANY item is actually processed.

**Fix:**
```javascript
async function processItems(items) {
  await Promise.all(items.map(item => processItem(item)))
  // OR: for (const item of items) { await processItem(item) }
  console.log('All processed!')
}
```

---

## 🔗 Navigation

**Prev:** [01_JS_Interview_Core.md](01_JS_Interview_Core.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [03_Coding_Problems.md](03_Coding_Problems.md)
