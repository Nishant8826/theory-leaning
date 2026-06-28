# 🚀 Interview Preparation - JS Output Questions

> **Domain:** Frontend & Backend JavaScript Development  
> **Level:** Beginner to Expert  
> **Target Role:** Software Engineer / Senior Engineer / Lead Javascript Developer

---

## 🟢 Beginner Level

### ❓ Q1. **Identify the output of the following `typeof` checks:**

```javascript
console.log(typeof null);
console.log(typeof []);
console.log(typeof (() => {}));
console.log(typeof NaN);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
"object"
"object"
"function"
"number"
```

**Explanation:**
- `typeof null` is `"object"` because of a historical bug in the initial JavaScript implementation where values were stored in 32-bit units with a type tag, and the tag for objects matched null (all zeros).
- `typeof []` is `"object"` because arrays are objects under the hood. To verify if a variable is a true array, use `Array.isArray(variable)`.
- `typeof (() => {})` is `"function"` because functions are first-class callable objects in JS.
- `typeof NaN` (Not a Number) is `"number"` because it is a numeric value representing an undefined or unrepresentable value in IEEE 754 float specs.

> 💡 **Interviewer Focus:** Standard JS typing quirks and how to safely check for null, arrays, and NaN (`isNaN()` or `Number.isNaN()`).

</details>

<hr/>

### ❓ Q2. **Explain the output of this hoisting snippet:**

```javascript
console.log(a);
console.log(b);

var a = 10;
let b = 20;
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
undefined
ReferenceError: Cannot access 'b' before initialization
```

**Explanation:**
- Variables declared with `var` are hoisted and initialized with a value of `undefined`. Hence, `console.log(a)` runs without error and prints `undefined`.
- Variables declared with `let` and `const` are hoisted but **not initialized**. They reside in the **Temporal Dead Zone (TDZ)** from the start of the block until the execution reaches the line where they are declared. Accessing them inside this window throws a `ReferenceError`.

> 💡 **Interviewer Focus:** Explain what the Temporal Dead Zone (TDZ) is and how hoisting differs between `var` and block-scoped (`let`/`const`) variables.

</details>

<hr/>

### ❓ Q3. **Identify the output of the following string additions:**

```javascript
console.log(1 + "2" + 3);
console.log(1 + 2 + "3");
console.log("1" + 2 + 3);
console.log(1 + + "2" + 3);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
"123"
"33"
"123"
"6"
```

**Explanation:**
- `1 + "2" + 3`: Operators execute left-to-right. `1 + "2"` coerces 1 to a string resulting in `"12"`. Then `"12" + 3` results in `"123"`.
- `1 + 2 + "3"`: First, the numbers `1 + 2` are added resulting in numeric `3`. Then `3 + "3"` coerces 3 to a string, resulting in `"33"`.
- `"1" + 2 + 3`: `"1" + 2` becomes `"12"`, then `"12" + 3` becomes `"123"`.
- `1 + + "2" + 3`: The unary plus operator `+ "2"` converts the string `"2"` to the number `2`. The expression evaluates as `1 + 2 + 3`, resulting in the number `6`.

> 💡 **Interviewer Focus:** Implicit type coercion rules and the role of the unary plus operator.

</details>

<hr/>

### ❓ Q4. **Identify the output of these equality evaluations:**

```javascript
console.log(0 == false);
console.log(0 === false);
console.log("" == false);
console.log(null == undefined);
console.log(null === undefined);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
true
false
true
true
false
```

**Explanation:**
- `0 == false`: Double equals (`==`) performs type coercion. Both values are coerced to numbers, resolving as `0 == 0`, which is `true`.
- `0 === false`: Triple equals (`===`) checks both value and type. `number` vs `boolean` evaluates to `false`.
- `"" == false`: Both are coerced to numbers, resolving as `0 == 0` (`true`).
- `null == undefined`: A special rule in the ECMAScript spec dictates that `null` and `undefined` are loosely equal to each other (and to nothing else).
- `null === undefined`: Since their types are different (`object` vs `undefined`), it evaluates to `false`.

> 💡 **Interviewer Focus:** Truthy/Falsy values and why developers should default to `===` in production code.

</details>

<hr/>

### ❓ Q5. **Explain the output of this array comparison:**

```javascript
const a = [];
const b = [];
console.log(a == b);
console.log(a === b);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
false
false
```

**Explanation:**
- In JavaScript, objects, arrays, and functions are compared by **reference (memory address)**, not by value.
- Even though `a` and `b` are empty arrays, they are stored in separate memory locations. Hence, their references are different, resulting in `false` for both comparisons.

> 💡 **Interviewer Focus:** Reference-based equality in objects/arrays vs value-based equality in primitives.

</details>

<hr/>

### ❓ Q6. **What is the output of the following delete operations?**

```javascript
const user = { name: "Alice" };
let age = 25;

console.log(delete user.name);
console.log(delete age);
console.log(user);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
true
false
{}
```

**Explanation:**
- The `delete` operator is designed to delete properties from objects. `delete user.name` successfully removes the property and returns `true`.
- You cannot delete variables declared using `let`, `const`, or `var`. `delete age` returns `false` (or throws a syntax error in strict mode).

> 💡 **Interviewer Focus:** The mechanics of the `delete` operator and strict mode constraints.

</details>

<hr/>

### ❓ Q7. **Explain the output of this nested scope variable shadowing snippet:**

```javascript
let x = 10;
function foo() {
  let x = 20;
  if (true) {
    let x = 30;
    console.log(x);
  }
  console.log(x);
}
foo();
console.log(x);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
30
20
10
```

**Explanation:**
- JavaScript features block scope for variables declared with `let`.
- Each nested block redeclares its own local variable `x`, shadowing variables with the same name in parent scopes.
- The inner console logs `30`, the function scope logs `20`, and the outer global scope logs `10`.

> 💡 **Interviewer Focus:** Understanding block scoping and lexical variable shadowing.

</details>

<hr/>

### ❓ Q8. **Explain the output of this object key evaluation snippet:**

```javascript
const a = {};
const b = { key: "b" };
const c = { key: "c" };

a[b] = 123;
a[c] = 456;

console.log(a[b]);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
456
```

**Explanation:**
- Object keys in JavaScript must be strings or Symbols. If an object is used as a key, it is implicitly stringified by calling `.toString()`.
- Stringifying a plain object results in the string `"[object Object]"`.
- Therefore, both statements write to the same property key:
  - `a[b] = 123` becomes `a["[object Object]"] = 123`.
  - `a[c] = 456` becomes `a["[object Object]"] = 456` (overwriting the value).
- `a[b]` retrieves `a["[object Object]"]`, which returns `456`.

> 💡 **Interviewer Focus:** Implicit key stringification in JS objects, and mentioning modern `Map` collections as a solution for using non-string keys.

</details>

<hr/>

### ❓ Q9. **Identify the output of the following `this` binding snippet:**

```javascript
const obj = {
  name: "Nishant",
  getNameRegular() {
    return this.name;
  },
  getNameArrow: () => {
    return this.name;
  }
};

console.log(obj.getNameRegular());
console.log(obj.getNameArrow());
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
"Nishant"
undefined (or window.name value in browser environments)
```

**Explanation:**
- `getNameRegular` is a standard method. Its `this` is determined at execution time by the object calling it (`obj`), returning `"Nishant"`.
- `getNameArrow` is an arrow function. Arrow functions do **not** have their own `this` binding. They inherit `this` lexically from their surrounding enclosing scope. In this case, the surrounding scope is the global window/global object context where `this.name` is undefined.

> 💡 **Interviewer Focus:** Differences in `this` binding behavior between regular functions and arrow functions.

</details>

<hr/>

### ❓ Q10. **Explain the output of this return statement behavior:**

```javascript
function foo() {
  return
  {
    status: "OK"
  };
}
console.log(foo());
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
undefined
```

**Explanation:**
- JavaScript has an automatic semicolon insertion (ASI) engine.
- Because there is nothing on the line containing `return`, ASI automatically places a semicolon there, translating the code into `return;`.
- The code block `{ status: "OK" }` below it is treated as an unreachable code block. The function returns `undefined`.
- **Solution:** Place the opening curly brace `{` on the same line as the `return` keyword.

> 💡 **Interviewer Focus:** Automatic Semicolon Insertion (ASI) engine rules.

</details>

<hr/>

### ❓ Q11. **Identify the output of `console.log(1 < 2 < 3)` vs `console.log(3 > 2 > 1)`.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
true
false
```

**Explanation:**
- `1 < 2 < 3`: Evaluates left-to-right. `1 < 2` is `true`. The expression becomes `true < 3`. In numeric coercion, `true` evaluates as `1`, so `1 < 3` is `true`.
- `3 > 2 > 1`: `3 > 2` is `true`. The expression becomes `true > 1`. Coercing `true` to `1` evaluates `1 > 1`, which is `false`.

> 💡 **Interviewer Focus:** Comparison operations chaining and boolean-to-number coercion.

</details>

<hr/>

### ❓ Q12. **Identify the output of `console.log([] + [])` and `console.log([] + {})`.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
"" (empty string)
"[object Object]"
```

**Explanation:**
- The addition operator `+` triggers string coercion if either operand is not a number.
- `[] + []`: Empty arrays convert to empty strings `""`. Thus, `"" + ""` results in `""`.
- `[] + {}`: `[]` converts to `""`, and `{}` converts to its string representation `"[object Object]"`. Thus, `"" + "[object Object]"` results in `"[object Object]"`.

> 💡 **Interviewer Focus:** Coercion patterns of objects/arrays during additions.

</details>

<hr/>

### ❓ Q13. **Explain what happens when we do `const x = (1, 2, 3); console.log(x);`.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
3
```

**Explanation:**
- The **comma operator (`,`)** evaluates each of its operands from left to right and returns the value of the **last operand**.
- Therefore, the expression `(1, 2, 3)` evaluates `1`, then `2`, then `3`, and returns `3` to be assigned to `x`.

> 💡 **Interviewer Focus:** Comma operator mechanics.

</details>

<hr/>

### ❓ Q14. **What is the output of `console.log("5" - 3)` vs `console.log("5" + 3)`?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
2
"53"
```

**Explanation:**
- `"5" - 3`: The subtraction operator `-` only exists for numbers. JavaScript implicitly coerces the string `"5"` to the number `5`, resulting in `5 - 3 = 2`.
- `"5" + 3`: The addition operator `+` is overloaded for string concatenation. Since one operand is a string, the number `3` is coerced to the string `"3"`, resulting in `"53"`.

> 💡 **Interviewer Focus:** Subtraction vs addition coercion behaviors.

</details>

<hr/>

### ❓ Q15. **What is the output of `console.log(Boolean(null))` and `console.log(!!undefined)`?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
false
false
```

**Explanation:**
- `null` and `undefined` are natively **falsy** values in JavaScript.
- `Boolean(null)` converts `null` directly to its boolean value `false`.
- The double negation `!!` coerces values to boolean. `!undefined` yields `true`, and `!true` yields `false`.

> 💡 **Interviewer Focus:** The list of falsy values in JS (`false`, `0`, `""`, `null`, `undefined`, `NaN`).

</details>

<hr/>

### ❓ Q16. **Explain what is logged here:**

```javascript
let a = 1;
let b = a++;
console.log(a, b);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
2 1
```

**Explanation:**
- The postfix increment operator `a++` increments the variable `a` by `1` but returns the **original value** before the increment.
- Therefore, `b` is assigned the original value of `a` (`1`), while `a` is incremented to `2`.

> 💡 **Interviewer Focus:** Postfix vs prefix (`++a`) increment operations.

</details>

<hr/>

### ❓ Q17. **What is the output of `console.log(typeof NaN === "number")`?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
true
```

**Explanation:**
- Even though `NaN` means "Not a Number", its numeric value type representation in JavaScript's type system is strictly `"number"`.

> 💡 **Interviewer Focus:** NaN properties.

</details>

<hr/>

### ❓ Q18. **Explain the output of this scope comparison:**

```javascript
{
  var x = 1;
  let y = 2;
}
console.log(x);
console.log(y);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
1
ReferenceError: y is not defined
```

**Explanation:**
- `var` is function-scoped (or globally scoped if declared outside a function). It ignores standard curly brace block boundaries, so `x` is accessible outside the block.
- `let` is block-scoped. It exists only within the curly braces `{ ... }` where it was declared, throwing a `ReferenceError` when accessed outside.

> 💡 **Interviewer Focus:** Function scope vs block scope.

</details>

<hr/>

### ❓ Q19. **What is the output of `console.log(Number.isInteger(1.0))` vs `console.log(Number.isInteger(1.1))`?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
true
false
```

**Explanation:**
- In JavaScript, all numbers are double-precision floating-point numbers (IEEE 754).
- `1.0` has no fractional component, so it is treated mathematically and logically as an integer by `Number.isInteger()`.
- `1.1` has a fractional component, returning `false`.

> 💡 **Interviewer Focus:** Representation of numbers in JS.

</details>

<hr/>

### ❓ Q20. **What is logged here?**

```javascript
let name = "Alice";
function sayHello() {
  console.log("Hello " + name);
}
name = "Bob";
sayHello();
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
"Hello Bob"
```

**Explanation:**
- The function `sayHello` creates a closure over the outer lexical scope.
- It holds a reference to the active variable `name`, not a snapshot copy of its value when the function was created.
- Since `name` is updated to `"Bob"` before the function is called, it prints `"Hello Bob"`.

> 💡 **Interviewer Focus:** Closures referencing active scope variables.

</details>

<hr/>

### ❓ Q21. **What is the output of `console.log(0.1 + 0.2 === 0.3)`?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
false
```

**Explanation:**
- JavaScript numbers are binary floating-point representations. Fractions like `0.1` and `0.2` cannot be represented precisely in binary, leading to rounding errors.
- `0.1 + 0.2` evaluates to `0.30000000000000004`, which is not strictly equal to `0.3`.

> 💡 **Interviewer Focus:** Floating-point arithmetic errors and how to check equality using `Number.EPSILON`.

</details>

<hr/>

### ❓ Q22. **What does this output?**

```javascript
const obj = { prop: 42 };
Object.freeze(obj);
obj.prop = 33;
console.log(obj.prop);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
42
```

**Explanation:**
- `Object.freeze()` makes an object immutable. It prevents adding, deleting, or modifying properties.
- Property modifications fail silently in non-strict mode (and throw a TypeError in strict mode).

> 💡 **Interviewer Focus:** Freezing objects.

</details>

<hr/>

### ❓ Q23. **What is the output of `console.log(typeof (typeof 1))`?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
"string"
```

**Explanation:**
- `typeof 1` returns the string `"number"`.
- Then, `typeof "number"` evaluates to `"string"`.

> 💡 **Interviewer Focus:** Precedence and typing.

</details>

<hr/>

### ❓ Q24. **Identify the output of this loop execution:**

```javascript
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
3
3
3
```

**Explanation:**
- `var` is function-scoped. The loop executes and increments `i` to `3`.
- The `setTimeout` callbacks run asynchronously after the loop finishes. All three closures reference the same shared variable `i`, which is now `3`.

> 💡 **Interviewer Focus:** Hoisting in loop contexts.

</details>

<hr/>

### ❓ Q25. **What is the output of `console.log(null == 0)`?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
false
```

**Explanation:**
- In loose equality comparisons (`==`), `null` is only equal to `undefined` or itself. It is not coerced to a number (unlike boolean comparisons), so `null == 0` evaluates to `false`.

> 💡 **Interviewer Focus:** Quirks of null comparison logic.

</details>

<hr/>

## 🟡 Intermediate Level

### ❓ Q26. **Explain the output of this closure variable iteration snippet:**

```javascript
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}

for (let j = 0; j < 3; j++) {
  setTimeout(() => console.log(j), 100);
}
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
3
3
3
0
1
2
```

**Explanation:**
- **`var i`**: `var` is function-scoped. The loop runs, updating the single shared variable `i` to `3`. The `setTimeout` callbacks run after the loop completes, referencing this single shared `i` variable whose value is now `3`.
- **`let j`**: `let` is block-scoped. During every loop iteration, a new lexical block scope is created with its own unique version of `j`. Each `setTimeout` closure captures a different reference of `j` at that iteration (`0`, `1`, and `2`).

> 💡 **Interviewer Focus:** Scope difference between `var` and `let` during loops, and closure capturing concepts.

</details>

<hr/>

### ❓ Q27. **Explain the output of this prototypal creation snippet:**

```javascript
const parent = {
  data: [1, 2],
  val: 10
};

const child = Object.create(parent);
child.data.push(3);
child.val = 20;

console.log(parent.data);
console.log(parent.val);
console.log(child.val);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
[1, 2, 3]
10
20
```

**Explanation:**
- `Object.create(parent)` creates a new empty object `child` with its prototype set to `parent`.
- `child.data` accesses the `data` array. Since `child` does not have a local property named `data`, it walks up the prototype chain to find it on `parent`. `child.data.push(3)` mutates the shared array located on the prototype (`parent`), affecting `parent.data`.
- `child.val = 20` writes a new local property `val` directly on the `child` object. It does not modify `parent.val` (property shadowing). Thus, `parent.val` remains `10` and `child.val` reads `20`.

> 💡 **Interviewer Focus:** Prototype lookup mechanism, reference types mutation vs primitive property shadowing.

</details>

<hr/>

### ❓ Q28. **Explain the execution sequence of this Event Loop snippet:**

```javascript
console.log("Start");

setTimeout(() => {
  console.log("Timeout");
}, 0);

Promise.resolve().then(() => {
  console.log("Promise");
});

console.log("End");
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
Start
End
Promise
Timeout
```

**Explanation:**
1. Synchronous operations run first: `console.log("Start")` and `console.log("End")` print immediately.
2. `setTimeout(..., 0)` registers a callback to the **Macrotask Queue** (or Task Queue).
3. `Promise.resolve().then(...)` registers a callback to the **Microtask Queue**.
4. Once the current synchronous call stack clears, the Event Loop processes the entire **Microtask Queue** *before* running any tasks from the Macrotask Queue.
5. Thus, the `"Promise"` callback executes first, followed by the `"Timeout"` callback.

> 💡 **Interviewer Focus:** Microtask queue (Promises, queueMicrotask) priority over Macrotask queue (setTimeout, setInterval).

</details>

<hr/>

### ❓ Q29. **What is the output of this explicit binding invocation?**

```javascript
function greet() {
  return `Hello, ${this.name}`;
}

const obj1 = { name: "Alice" };
const obj2 = { name: "Bob" };

const greetAlice = greet.bind(obj1);
console.log(greetAlice());
console.log(greetAlice.call(obj2));
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
"Hello, Alice"
"Hello, Alice"
```

**Explanation:**
- `greet.bind(obj1)` creates a new bound function `greetAlice` with its `this` permanently set to `obj1`.
- A function created with `.bind()` cannot have its context changed by subsequent calls to `.call()` or `.apply()`. The secondary `.call(obj2)` is ignored, returning the original bound reference of `Alice`.

> 💡 **Interviewer Focus:** Permanence of `Function.prototype.bind()` bindings.

</details>

<hr/>

### ❓ Q30. **Explain the output of this object reference copy snippet:**

```javascript
const user1 = {
  name: "John",
  address: { city: "Delhi" }
};

const user2 = { ...user1 };
user2.name = "David";
user2.address.city = "Mumbai";

console.log(user1.name);
console.log(user1.address.city);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
"John"
"Mumbai"
```

**Explanation:**
- The spread operator `{ ...user1 }` performs a **shallow copy** of the object.
- The primitive value `name` is copied. Modifying `user2.name` has no effect on `user1.name`.
- The nested object `address` is copied by **reference**, meaning both `user1.address` and `user2.address` point to the exact same object in memory.
- Therefore, changing `user2.address.city` updates the shared object, mutating `user1.address.city` as well.

> 💡 **Interviewer Focus:** Shallow copy vs Deep copy difference and how to perform deep copies in modern JS (e.g. `structuredClone()`).

</details>

<hr/>

### ❓ Q31. **Identify the output of this array destructuring default values snippet:**

```javascript
const [a = 1, b = 2, c = 3] = [null, undefined];
console.log(a, b, c);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
null 2 3
```

**Explanation:**
- JavaScript destructuring uses default fallback values *only* when properties/elements evaluate strictly to `undefined`.
- The first element is `null`. Since `null` is a valid value, `a` is bound to `null` (the default `1` is ignored).
- The second element is `undefined`. Because it is undefined, `b` falls back to its default value `2`.
- The third element does not exist in the array (evaluates as `undefined`), so `c` falls back to its default value `3`.

> 💡 **Interviewer Focus:** Understanding that destructuring default fallbacks trigger only on `undefined` values, not `null` values.

</details>

<hr/>

### ❓ Q32. **What is logged after executing this sparse array map process?**

```javascript
const arr = [1, , 3];
const result = arr.map(x => x * 2);
console.log(result);
console.log(result.length);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
[2, empty, 6] (or [2, undefined, 6] depending on console display formatting)
3
```

**Explanation:**
- `arr` is a sparse array containing an empty slot (a hole) at index 1.
- Array methods like `map()`, `filter()`, and `forEach()` skip empty slots in sparse arrays, preserving the holes in the returned array without calling the callback function for them.
- However, the size/length of the array remains unchanged (`3`).

> 💡 **Interviewer Focus:** Handling sparse arrays and knowing how array iteration methods skip empty indexes.

</details>

<hr/>

### ❓ Q33. **Explain the output of this parameter mutation snippet:**

```javascript
function modify(a, b) {
  a = 100;
  b.value = 200;
}

let num = 10;
let obj = { value: 20 };

modify(num, obj);

console.log(num);
console.log(obj.value);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
10
200
```

**Explanation:**
- In JavaScript, arguments are passed to functions by **value**.
- For primitives (like `num`), the value `10` is copied into local variable `a`. Mutating `a` has no effect on `num`.
- For objects, the reference address is copied by value. Therefore, `b` points to the same object in memory as `obj`. Mutating properties on `b` (`b.value = 200`) modifies the shared object, mutating the outer variable `obj.value`.

> 💡 **Interviewer Focus:** Pass-by-value of references mechanics in JS.

</details>

<hr/>

### ❓ Q34. **What is the output of this arrow function arguments evaluation?**

```javascript
function regular() {
  const arrow = () => {
    console.log(arguments[0]);
  };
  arrow("inner");
}
regular("outer");
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
"outer"
```

**Explanation:**
- Arrow functions do **not** have their own local `arguments` object.
- If referenced inside an arrow function, it inherits the `arguments` object lexically from its parent regular function scope.
- In this case, `arguments[0]` evaluates to the first parameter of the parent `regular` function call, printing `"outer"`.

> 💡 **Interviewer Focus:** Lexical scoping of special identifiers in arrow functions.

</details>

<hr/>

### ❓ Q35. **What is the output of this operator precedence expression?**

```javascript
console.log(typeof typeof 123);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
"string"
```

**Explanation:**
- `typeof 123` executes first, returning the string value `"number"`.
- The expression then evaluates to `typeof "number"`.
- Since `"number"` is a string, `typeof` returns `"string"`.

> 💡 **Interviewer Focus:** Understanding that `typeof` always returns a string representation of the type.

</details>

<hr/>

### ❓ Q36. **Identify the output of `console.log(2 + true)` and `console.log("2" - true)`.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
3
1
```

**Explanation:**
- `2 + true`: Addition coerces the boolean `true` to the number `1`, returning `2 + 1 = 3`.
- `"2" - true`: Subtraction forces numeric conversion. The string `"2"` is converted to number `2`, and boolean `true` is converted to number `1`, returning `2 - 1 = 1`.

> 💡 **Interviewer Focus:** Boolean coercion to binary values (`true` = 1, `false` = 0) in math operations.

</details>

<hr/>

### ❓ Q37. **What is the output of `console.log([1, 2] + [3, 4])`?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
"1,23,4"
```

**Explanation:**
- The `+` operator trigger string coercion.
- `[1, 2]` converts to the string `"1,2"`.
- `[3, 4]` converts to the string `"3,4"`.
- Concatenating `"1,2" + "3,4"` results in `"1,23,4"`.

> 💡 **Interviewer Focus:** Array-to-string coercion mechanics.

</details>

<hr/>

### ❓ Q38. **Explain the output of this object reference check:**

```javascript
const x = { val: 1 };
const y = x;
y.val = 2;
console.log(x.val);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
2
```

**Explanation:**
- In JavaScript, assigning one object variable to another (`y = x`) copies the **memory address reference**, not the value.
- Both `x` and `y` reference the exact same object in heap memory. Mutating `y.val` automatically modifies `x.val`.

> 💡 **Interviewer Focus:** Object pointers.

</details>

<hr/>

### ❓ Q39. **Identify the output of `console.log(parseInt("10px"))` vs `console.log(Number("10px"))`.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
10
NaN
```

**Explanation:**
- `parseInt("10px")` parses characters left-to-right, extracting numeric characters until it hits a non-numeric character (`p`), returning `10`.
- `Number("10px")` evaluates the *entire* string structure strictly. Since `"10px"` is not a valid number format, it returns `NaN`.

> 💡 **Interviewer Focus:** Lenient parsing (`parseInt`) vs strict numeric conversion (`Number`).

</details>

<hr/>

### ❓ Q40. **What is the output of `console.log(Array.isArray(Array.prototype))`?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
true
```

**Explanation:**
- In the ECMAScript specification, `Array.prototype` is itself an **array** (specifically, an empty array), designed to host array utility methods.

> 💡 **Interviewer Focus:** Prototype properties typing.

</details>

<hr/>

### ❓ Q41. **Identify the output of this function invocation:**

```javascript
function foo(a, a, b) {
  console.log(a, b);
}
foo(1, 2, 3);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
2 3
```

**Explanation:**
- In non-strict mode, duplicate parameter names are allowed. The last duplicate parameter (`a`) overrides the value of the previous ones.
- Therefore, the second argument (`2`) binds to `a`, overwriting the first argument (`1`).
- *Note: Duplicate parameter names throw a SyntaxError in strict mode.*

> 💡 **Interviewer Focus:** Parameter resolution behaviors in strict vs non-strict mode.

</details>

<hr/>

### ❓ Q42. **Explain the output of this recursive addition snippet:**

```javascript
let count = 0;
(function immediate() {
  if (count === 0) {
    let count = 1;
    console.log(count);
  }
  console.log(count);
})();
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
1
0
```

**Explanation:**
- The immediate function accesses the global `count` (`0`) in its condition.
- Inside the `if` block, a new block-scoped variable `count` is declared using `let count = 1`. This shadows the outer variable, printing `1` inside.
- Once control exits the block, the local shadow variable is discarded, and the outer `count` (`0`) is printed.

> 💡 **Interviewer Focus:** Lexical block scope shadowing.

</details>

<hr/>

### ❓ Q43. **Identify the output of `console.log(Math.max())` vs `console.log(Math.min())`.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
-Infinity
Infinity
```

**Explanation:**
- `Math.max()` returns the largest number of the passed arguments. If no arguments are provided, the baseline starts at the lowest possible numeric representation: **`-Infinity`**.
- `Math.min()` returns the smallest number. If no arguments are provided, the baseline starts at **`Infinity`**.

> 💡 **Interviewer Focus:** JavaScript mathematical boundaries.

</details>

<hr/>

### ❓ Q44. **What is logged here?**

```javascript
const arr = [10, 20, 30];
arr[10] = 100;
console.log(arr.length);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
11
```

**Explanation:**
- Assigning a value to an index higher than the current size dynamically scales the array.
- The array creates empty "holes" at indexes 3-9, and sets index 10 to `100`. The `length` property is updated to match the highest index plus one (`10 + 1 = 11`).

> 💡 **Interviewer Focus:** Dynamic array scaling and sparse indexes.

</details>

<hr/>

### ❓ Q45. **What is the output of `console.log(typeof NaN)`?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
"number"
```

**Explanation:**
- `NaN` stands for "Not a Number", but in JavaScript, it is a numeric value representing an undefined result, returning `"number"`.

> 💡 **Interviewer Focus:** IEEE 754 representations.

</details>

<hr/>

### ❓ Q46. **Explain the output of this strict equality validation:**

```javascript
console.log(NaN === NaN);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
false
```

**Explanation:**
- According to IEEE 754 float specs, `NaN` is not equal to any value, including itself.
- To check if a value is NaN, you must use `Number.isNaN()` or `Object.is(val, NaN)`.

> 💡 **Interviewer Focus:** NaN comparison rules.

</details>

<hr/>

### ❓ Q47. **What is logged by executing this function call?**

```javascript
function test() {
  console.log(x);
  var x = 10;
}
test();
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
undefined
```

**Explanation:**
- The variable `x` is declared using `var`, which hoists the declaration to the top of the function scope and initializes it to `undefined`.
- Accessing it before assignment prints `undefined`.

> 💡 **Interviewer Focus:** Variable hoisting.

</details>

<hr/>

### ❓ Q48. **Identify the output of `console.log("b" + "a" + + "a" + "a").toLowerCase()`.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
"banana"
```

**Explanation:**
- The expression evaluates as: `"b"` + `"a"` + `+ "a"` + `"a"`.
- The unary plus `+ "a"` tries to convert the string `"a"` to a number, returning `NaN`.
- The expression becomes `"ba"` + `NaN` + `"a"`, which concatenates to `"baNaNa"`.
- Calling `.toLowerCase()` converts it to `"banana"`.

> 💡 **Interviewer Focus:** Coercion quirks.

</details>

<hr/>

### ❓ Q49. **What is the output of `console.log(1 && 2)` and `console.log(0 || 3)`?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
2
3
```

**Explanation:**
- **`&&` (Logical AND):** Returns the first falsy operand, or the last operand if all are truthy. Since `1` is truthy, it returns `2`.
- **`||` (Logical OR):** Returns the first truthy operand. Since `0` is falsy, it checks the next operand and returns `3`.

> 💡 **Interviewer Focus:** Logical short-circuiting rules.

</details>

<hr/>

### ❓ Q50. **Identify what is logged:**

```javascript
const obj = { a: 1 };
console.log("toString" in obj);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
true
```

**Explanation:**
- The `in` operator checks for the existence of a property on the target object **or its prototype chain**.
- Although `"toString"` is not defined on `obj` directly, it is inherited from `Object.prototype`, returning `true`.

> 💡 **Interviewer Focus:** Prototypal inheritance lookup via the "in" operator.

</details>

<hr/>

## 🔴 Advanced Level

### ❓ Q51. **Explain the interleaved execution output of this Microtask and Macrotask sequence:**

```javascript
console.log("1");

setTimeout(() => console.log("2"), 0);

Promise.resolve().then(() => {
  console.log("3");
  setTimeout(() => console.log("4"), 0);
  Promise.resolve().then(() => console.log("5"));
});

Promise.resolve().then(() => console.log("6"));

console.log("7");
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
1
7
3
6
5
2
4
```

**Explanation:**
1. **Sync Stage:** Prints `1` and `7`.
2. **Macrotask Queue:** `[ Timeout 2 ]`
3. **Microtask Queue:** `[ Promise 3, Promise 6 ]`
4. **Flush Microtasks:**
   - Execute `Promise 3`: Prints `3`. Enqueues a new macro `Timeout 4` and a new micro `Promise 5`.
     - Macrotask Queue: `[ Timeout 2, Timeout 4 ]`
     - Microtask Queue: `[ Promise 6, Promise 5 ]`
   - Execute `Promise 6`: Prints `6`.
   - Execute `Promise 5`: Prints `5`.
5. **Event Loop executes Macrotasks:**
   - Run first macro `Timeout 2`: Prints `2`.
   - Run second macro `Timeout 4`: Prints `4`.

> 💡 **Interviewer Focus:** Trace the exact interleaving of microtasks generated during microtask flushes.

</details>

<hr/>

### ❓ Q52. **Explain the execution sequence of this Async/Await execution chain:**

```javascript
async function async1() {
  console.log("async1 start");
  await async2();
  console.log("async1 end");
}

async function async2() {
  console.log("async2");
}

console.log("script start");
async1();
console.log("script end");
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
script start
async1 start
async2
script end
async1 end
```

**Explanation:**
1. Prints `"script start"`.
2. Calls `async1()`. Prints `"async1 start"`.
3. Calls `await async2()`.
   - In JS, async functions run synchronously *until* they hit the first `await` keyword.
   - It runs `async2()` synchronously, printing `"async2"`.
   - The execution of the rest of `async1()` (after the await) is suspended and scheduled as a **microtask** (equivalent to a `.then()` resolution).
4. Control returns to the main stack. Prints `"script end"`.
5. The synchronous call stack clears. The event loop checks the microtask queue, resuming `async1()` and printing `"async1 end"`.

> 💡 **Interviewer Focus:** Microtask conversion of operations following the `await` keyword.

</details>

<hr/>

### ❓ Q53. **What is the output of this Temporal Dead Zone (TDZ) parameter evaluation?**

```javascript
let x = 1;
function foo(y = x, x = 2) {
  console.log(y);
}
foo();
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
ReferenceError: Cannot access 'x' before initialization
```

**Explanation:**
- Function parameter scopes form their own block scope environments when default parameter bindings are used.
- The parameters are evaluated left-to-right:
  - First, `y` tries to resolve to its default value `x`.
  - However, `x` is declared as the *second* parameter `x = 2`.
  - Since parameters reside in the TDZ before initialization, referencing `x` before its declaration line (even though there is a global `let x = 1` outside) throws a `ReferenceError` because the local parameter shadowing variable `x` is accessed before initialization.

> 💡 **Interviewer Focus:** Function parameter scopes and parameterTDZ rules.

</details>

<hr/>

### ❓ Q54. **Explain the output of this prototype descriptor assignment:**

```javascript
const obj = {};
Object.defineProperty(obj, "prop", {
  value: 42,
  writable: false
});

const child = Object.create(obj);
child.prop = 99;

console.log(child.prop);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
42
```

**Explanation:**
- `Object.defineProperty` configures a property descriptor with `writable: false`.
- `child` inherits `prop` via the prototype chain.
- If a property on the prototype chain is configured as **non-writable**, JavaScript blocks the creation of an overriding property of the same name on the child object via assignment (`child.prop = 99`). This action fails silently in non-strict mode (and throws a TypeError in strict mode).
- Thus, `child.prop` continues to read the prototype's value of `42`.

> 💡 **Interviewer Focus:** Side-effects of prototype descriptors on inheritance property shadowing.

</details>

<hr/>

### ❓ Q55. **Explain the output of this WeakMap garbage collection logic:**

```javascript
let map = new WeakMap();
let obj = { name: "test" };

map.set(obj, "metadata");
obj = null;

// Imagine garbage collection runs here
console.log(map.has(obj));
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
false
```

**Explanation:**
- `WeakMap` keys must be objects. The references to these keys are held **weakly**.
- If there are no other references left to the key object in memory (since we set `obj = null`), the key object becomes eligible for Garbage Collection.
- Once garbage collection runs, the key and its corresponding value are automatically removed from the WeakMap.
- Additionally, calling `map.has(obj)` with `null` resolves to `false` because `null` is not a valid key.

> 💡 **Interviewer Focus:** Memory leak prevention benefits of `WeakMap` vs `Map`.

</details>

<hr/>

### ❓ Q56. **What is the output of this generator function sequence?**

```javascript
function* gen() {
  const x = yield 1;
  const y = yield (x * 2);
  return y;
}

const g = gen();
console.log(g.next().value);
console.log(g.next(10).value);
console.log(g.next(20).value);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
1
20
20
```

**Explanation:**
1. The first `.next()` invocation starts the generator. It runs until it hits the first `yield 1`, returning a value of `1`.
2. The second `.next(10)` passes the value `10` *into* the generator. This value replaces the entire `yield 1` expression, setting `x = 10`. The generator runs until it hits `yield (x * 2)`, which evaluates to `yield 20`, returning a value of `20`.
3. The third `.next(20)` passes the value `20` into the generator, replacing the second yield statement and setting `y = 20`. The generator runs to the `return y` statement, returning the final value of `20` (marked as `done: true`).

> 💡 **Interviewer Focus:** Passing parameters dynamically into generator engines via `.next()`.

</details>

<hr/>

### ❓ Q57. **What is the output of this infinitecurry function?**

```javascript
function curry(x) {
  return function(y) {
    if (y !== undefined) {
      return curry(x + y);
    }
    return x;
  };
}

console.log(curry(1)(2)(3)());
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
6
```

**Explanation:**
- The `curry` function returns an inner function that expects a parameter `y`.
- If `y` is provided, it returns a new invocation of `curry` passing the accumulated sum `x + y`.
- If no argument is passed (i.e., `y` is `undefined`), the recursion chain breaks and returns the accumulated sum `x`.
- `curry(1)(2)(3)()` resolves sequentially to accumulate `1 + 2 + 3` and then evaluates as empty argument call, returning `6`.

> 💡 **Interviewer Focus:** Designing currying functions and closures for infinite argument list accumulation.

</details>

<hr/>

### ❓ Q58. **Explain what is logged in the following Symbol iteration snippet:**

```javascript
const sym = Symbol("secret");
const obj = {
  [sym]: "hidden",
  public: "visible"
};

console.log(Object.keys(obj));
console.log(JSON.stringify(obj));
console.log(Reflect.ownKeys(obj));
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
["public"]
'{"public":"visible"}'
["public", Symbol(secret)]
```

**Explanation:**
- Symbol properties do not show up in standard iteration methods like `Object.keys()`, `for...in` loops, or `Object.getOwnPropertyNames()`.
- They are also ignored during JSON stringification (`JSON.stringify()`).
- To retrieve Symbol properties, you must use `Object.getOwnPropertySymbols(obj)` or `Reflect.ownKeys(obj)` (which returns both string and symbol keys).

> 💡 **Interviewer Focus:** Using Symbols to declare pseudo-private properties on objects.

</details>

<hr/>

### ❓ Q59. **Identify what is logged here:**

```javascript
const obj = {};
Object.defineProperty(obj, "a", {
  value: 1,
  enumerable: false
});

const clone = { ...obj };
console.log(clone.a);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
undefined
```

**Explanation:**
- The spread operator `{ ...obj }` and `Object.assign()` only copy **enumerable** own properties.
- Since property `"a"` is explicitly configured with `enumerable: false`, it is ignored during the spread operation, resulting in an empty `clone` object.

> 💡 **Interviewer Focus:** Property descriptors configuration properties (enumerable, configurable, writable).

</details>

<hr/>

### ❓ Q60. **What is the output of this constructor binding evaluation?**

```javascript
function User(name) {
  this.name = name;
  return { custom: "Object" };
}

const u = new User("Alice");
console.log(u.name);
console.log(u.custom);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
undefined
"Object"
```

**Explanation:**
- When a function is called with the `new` operator, it creates a new empty object binded to `this` context.
- If the constructor returns an **object** explicitly, that returned object overrides the implicit instance creation object.
- If the constructor returns a primitive value (like a string or number), the primitive is ignored and the implicit `this` instance is returned.
- Since `User` returns `{ custom: "Object" }` (which is an object), this object is assigned to `u`. `u.name` is undefined.

> 💡 **Interviewer Focus:** Return overrides constraints inside `new` constructors.

</details>

<hr/>

### ❓ Q61. **What is the output of this Promise validation sequence?**

```javascript
Promise.resolve(1)
  .then(x => x + 1)
  .then(x => { throw x })
  .catch(x => x + 1)
  .then(x => console.log(x));
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
3
```

**Explanation:**
- `Promise.resolve(1)` initiates the chain with value `1`.
- The first `.then()` adds `1`, returning `2`.
- The second `.then()` throws the value `2`, causing the promise to reject with reason `2`.
- The `.catch()` intercepts the rejection. It receives `2` as parameter `x` and returns `x + 1 = 3`. Catch blocks return resolved promises by default if they return values without throwing.
- The third `.then()` receives the resolved value `3` and logs `3`.

> 💡 **Interviewer Focus:** Promise recovery mechanisms inside catch blocks.

</details>

<hr/>

### ❓ Q62. **Explain the output of this microtask chaining execution:**

```javascript
queueMicrotask(() => console.log("Micro1"));
Promise.resolve().then(() => console.log("Promise1"));
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
Micro1
Promise1
```

**Explanation:**
- Both `queueMicrotask` and `Promise.resolve().then` enqueue callbacks directly onto the same Microtask Queue.
- Therefore, they execute in the exact FIFO (First-In, First-Out) sequence in which they were declared.

> 💡 **Interviewer Focus:** Microtask queue ordering parity.

</details>

<hr/>

### ❓ Q63. **What is logged here?**

```javascript
const arr = [1, 2, 3];
const [x, , y] = arr;
console.log(x, y);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
1 3
```

**Explanation:**
- Array destructuring allows omitting elements by placing consecutive commas.
- `x` binds to index 0 (`1`).
- The empty slot `, ,` skips index 1.
- `y` binds to index 2 (`3`).

> 💡 **Interviewer Focus:** Selective array destructuring.

</details>

<hr/>

### ❓ Q64. **Explain what happens here:**

```javascript
let x = 1;
function test() {
  console.log(x);
  let x = 2;
}
test();
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
ReferenceError: Cannot access 'x' before initialization
```

**Explanation:**
- The function scope of `test` declares a local variable `x` using `let x = 2`.
- Although there is a global `x = 1` outside, the local `let` declaration hoists to the top of the function block, shadowing the outer variable.
- The local `x` is in the Temporal Dead Zone (TDZ) at the beginning of the function, so trying to log it before initialization throws a `ReferenceError`.

> 💡 **Interviewer Focus:** TDZ and shadowing.

</details>

<hr/>

### ❓ Q65. **Identify the output of `console.log(typeof Object)` vs `console.log(typeof Object.prototype)`.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
"function"
"object"
```

**Explanation:**
- `Object` is the standard constructor function wrapper, returning `"function"`.
- `Object.prototype` is the base prototype object containing utility methods like `.toString()`, returning `"object"`.

> 💡 **Interviewer Focus:** Built-in constructors and their prototype structures.

</details>

<hr/>

### ❓ Q66. **What is the output of `console.log(1 || 2 && 3)`?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
1
```

**Explanation:**
- Logical AND (`&&`) has higher operator precedence than logical OR (`||`).
- The expression is evaluated as `1 || (2 && 3)`.
- `2 && 3` evaluates to `3` (since both are truthy).
- The expression becomes `1 || 3`. Because `1` is truthy, the evaluation short-circuits and returns `1`.

> 💡 **Interviewer Focus:** Precedence of boolean operators.

</details>

<hr/>

### ❓ Q67. **Explain the output of this object method binding:**

```javascript
const obj = {
  val: 1,
  print() {
    setTimeout(function() {
      console.log(this.val);
    }, 100);
  }
};
obj.print();
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
undefined
```

**Explanation:**
- The inner callback function inside `setTimeout` is a standard, non-arrow function.
- In standard callbacks, `this` binds to the global execution context (window/global), which does not contain `val`, resulting in `undefined`.
- **Solution:** Use an arrow function, which binds `this` lexically.

> 💡 **Interviewer Focus:** Binding context loss in standard callbacks.

</details>

<hr/>

### ❓ Q68. **What does this output?**

```javascript
const f = () => { "use strict"; x = 10; };
f();
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
ReferenceError: x is not defined
```

**Explanation:**
- Under `"use strict"`, you cannot assign a value to a variable that has not been declared.
- Bypasses default behavior where undeclared assignments automatically create global variables, throwing a `ReferenceError`.

> 💡 **Interviewer Focus:** Strict mode restrictions.

</details>

<hr/>

### ❓ Q69. **Identify what is logged:**

```javascript
function foo() {}
console.log(foo.prototype.__proto__ === Object.prototype);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
true
```

**Explanation:**
- Every standard function has a `prototype` object (used for instances created with `new`).
- Since the prototype is a standard object, its internal prototype chain pointer `__proto__` references the base `Object.prototype`, returning `true`.

> 💡 **Interviewer Focus:** Prototype link references.

</details>

<hr/>

### ❓ Q70. **What is the output of this evaluation?**

```javascript
const target = { a: 1 };
const source = { get b() { return this.a; } };
Object.assign(target, source);
console.log(target.b);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
undefined
```

**Explanation:**
- `Object.assign()` does not copy getter functions themselves; it invokes the getter and copies the **resulting value**.
- When `source.b` is evaluated during assignment, `this` points to `source`. Since `source` does not contain `a` (`source.a` is undefined), the value `undefined` is copied to `target.b`.

> 💡 **Interviewer Focus:** Object.assign limitations on property descriptors.

</details>

<hr/>

### ❓ Q71. **What is logged here?**

```javascript
const s = new Set([1, 1, 2, 3]);
console.log(s.size);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
3
```

**Explanation:**
- A `Set` stores only unique values. Duplicate values (like the second `1`) are ignored.
- The set contains `[1, 2, 3]`, resulting in a size of `3`.

> 💡 **Interviewer Focus:** Deduplication.

</details>

<hr/>

### ❓ Q72. **What is the output of `console.log(parseInt(0.0000005))`?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
5
```

**Explanation:**
- `parseInt` expects a string. If a number is passed, it converts it to a string first.
- Numbers smaller than $10^{-6}$ are stringified in scientific notation (e.g. `0.0000005` becomes `"5e-7"`).
- `parseInt("5e-7")` parses left-to-right, stopping at the non-numeric character `e` and returning the initial number `5`.

> 💡 **Interviewer Focus:** Numeric stringification anomalies.

</details>

<hr/>

### ❓ Q73. **Explain the output of this array filter mapping combination:**

```javascript
const arr = [1, 2, 3];
arr.filter(x => x > 1).map(x => x * 2);
console.log(arr);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
[1, 2, 3]
```

**Explanation:**
- Functional array methods like `filter()` and `map()` are **pure methods**.
- They return new array outputs without mutating the original `arr` array. Since the output was not saved to a variable, `arr` remains `[1, 2, 3]`.

> 💡 **Interviewer Focus:** Immutability in functional array operations.

</details>

<hr/>

### ❓ Q74. **What is logged by executing this function?**

```javascript
const x = [1, 2];
const y = [...x];
console.log(x === y);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
false
```

**Explanation:**
- The spread operator `[...x]` clones the array, creating a new array in memory.
- Since they point to different memory addresses, reference equality `x === y` returns `false`.

> 💡 **Interviewer Focus:** Cloning references.

</details>

<hr/>

### ❓ Q75. **What is the output of `console.log(new String("a") === new String("a"))`?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
false
```

**Explanation:**
- Using the `new` keyword with the `String` constructor creates a new wrapper **object** instance in heap memory.
- Like all objects, they are compared by reference, returning `false`.

> 💡 **Interviewer Focus:** Wrapper constructors objects.

</details>

<hr/>

## 🟣 Expert Level

### ❓ Q76. **Explain the output of this nested double-microtask execution chain:**

```javascript
Promise.resolve().then(() => {
  console.log("A");
  Promise.resolve().then(() => console.log("B"));
}).then(() => {
  console.log("C");
});

Promise.resolve().then(() => {
  console.log("D");
});
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
A
D
B
C
```

**Explanation:**
1. **Initial Microtasks:** The Event Loop starts with the initial queue: `[ Then1 (contains A), Then2 (contains D) ]`.
2. **Execute Then1:** Prints `"A"`. Enqueues the nested microtask `"B"`. Since `Then1` resolves successfully, its chained `.then()` containing `"C"` is enqueued *after* `"B"`.
   - Current Microtask Queue: `[ Then2 (D), Then "B", Then "C" ]`
3. **Execute Then2 (D):** Prints `"D"`.
4. **Execute Then "B":** Prints `"B"`.
5. **Execute Then "C":** Prints `"C"`.

> 💡 **Interviewer Focus:** Tracing microtask scheduling execution queues when handling nested promise resolutions.

</details>

<hr/>

### ❓ Q77. **Explain the output of this ES Module circular dependency execution mock:**

```javascript
// a.js (Simulated ES Module load)
console.log("a starting");
import { bVal } from "./b.js";
export let aVal = "A_Value";
console.log("a finished, bVal is", bVal);

// b.js (Simulated ES Module load)
console.log("b starting");
import { aVal } from "./a.js";
export let bVal = "B_Value";
console.log("b finished, aVal is", aVal);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output (assuming a.js is the entry point):**
```text
b starting
ReferenceError: Cannot access 'aVal' before initialization
```

**Explanation:**
- In ES Modules (ESM), imports are statically resolved and parsed before runtime.
- When `a.js` imports `./b.js`, execution shifts to `b.js` immediately.
- `b.js` tries to import `aVal` from `a.js`. However, `a.js` has not executed past its import statement yet, meaning `aVal` is declared but has not been initialized (TDZ).
- Attempting to log `aVal` inside `b.js` triggers a `ReferenceError` because the variable is accessed before initialization.

> 💡 **Interviewer Focus:** Static bindings resolution in ESM circular dependencies vs dynamic exports in CommonJS.

</details>

<hr/>

### ❓ Q78. **Explain the output of this Proxy handler interceptor loop:**

```javascript
const target = { name: "Alice" };
const handler = {
  get(target, prop, receiver) {
    console.log(`Getting ${prop}`);
    return Reflect.get(target, prop, receiver);
  }
};

const proxy = new Proxy(target, handler);
const child = Object.create(proxy);

child.name;
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
"Getting name"
```

**Explanation:**
- `Object.create(proxy)` creates an object `child` whose prototype is the `proxy`.
- Accessing `child.name` triggers a lookup. Since `child` does not have an own property named `name`, it walks up the prototype chain to `proxy`.
- The `proxy` intercepts the get operation on itself, triggering the `get` trap in the `handler` with `target` as the base object and `receiver` set to `child`.
- This logs `"Getting name"` and returns the resolved property value.

> 💡 **Interviewer Focus:** The role of the `receiver` parameter in Proxy traps to preserve correct `this` bindings during prototypal inheritance lookup.

</details>

<hr/>

### ❓ Q79. **Identify what is logged during this garbage collection memory leaks simulation:**

```javascript
function makeLeaker() {
  const largeArray = new Array(1000000).fill("data");
  return function() {
    // This closure captures the surrounding lexical environment
    console.log("Leaker executed");
  };
}

const leak = makeLeaker();
// If we set leak = null, does largeArray get collected?
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Explanation:**
- The returned function is assigned to the global variable `leak`.
- Since `leak` holds a reference to the inner function closure, the entire lexical environment of `makeLeaker()` (which contains `largeArray`) must remain in memory.
- `largeArray` cannot be garbage collected because the closure maintains a reference to the scope context, potentially causing a memory leak if `leak` is retained long-term in the global execution state.
- **Garbage Collection:** Once we set `leak = null`, the closure is no longer reachable, allowing the garbage collector to reclaim both the closure and the captured `largeArray`.

> 💡 **Interviewer Focus:** Lexical environments lifecycle and how closures can cause unintended memory leaks.

</details>

<hr/>

### ❓ Q80. **Explain what is logged in this strict mode property configuration operation:**

```javascript
"use strict";
const obj = {};
Object.defineProperty(obj, "prop", {
  value: 42,
  configurable: false,
  writable: true
});

Object.defineProperty(obj, "prop", { writable: false });
console.log(obj.prop);

Object.defineProperty(obj, "prop", { configurable: true });
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
42
TypeError: Cannot redefine property: prop
```

**Explanation:**
- First redefinition: Changing `writable` from `true` to `false` is allowed even if `configurable` is `false`. It restricts permissions, which is permitted. `obj.prop` prints `42`.
- Second redefinition: Trying to change `configurable` back to `true` (or attempting to change a non-configurable property descriptor's attributes, except for reducing writability) throws a `TypeError`.

> 💡 **Interviewer Focus:** Strict rules surrounding `Object.defineProperty` on non-configurable properties.

</details>

<hr/>

### ❓ Q81. **Explain the output of this shared array buffer atomic operation:**

```javascript
const sab = new SharedArrayBuffer(1024);
const ta = new Int32Array(sab);

ta[0] = 5;
Atomics.add(ta, 0, 10);
console.log(ta[0]);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
15
```

**Explanation:**
- `SharedArrayBuffer` allocates raw memory shared across threads/workers.
- `Atomics.add(ta, 0, 10)` performs an atomic addition operation, thread-safely adding `10` to the value at index `0` (`5`), resulting in `15`.

> 💡 **Interviewer Focus:** Thread-safe memory access using the `Atomics` API.

</details>

<hr/>

### ❓ Q82. **Explain what happens during V8 compiler optimizations when object structures change dynamically.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Hidden Classes (Shapes):** V8 compiler assigns an internal "shape" class to objects. If objects are created with the exact same structure (same keys in same order), they share the same shape class.
- **Dynamic updates:** If keys are added dynamically (e.g. `obj.b = 2`), V8 creates a new shape transition. This degrades performance of **Inline Caches** (caching property lookups), causing V8 to fall back to slow dictionary lookups.
- **Best Practice:** Initialize all properties in constructor definitions to maintain consistent shapes.

> 💡 **Interviewer Focus:** Hidden classes transitions and inline caching optimizations in JS engines.

</details>

<hr/>

### ❓ Q83. **How does JavaScript handle function parameters evaluation with nested destructuring defaults?**

```javascript
function test({ a = 1, b = { c: 2 } } = {}) {
  console.log(a, b.c);
}
test({ b: {} });
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
1 undefined
```

**Explanation:**
- Passing `{ b: {} }` triggers parameter destructuring.
- Since `{ b: {} }` has no property `a`, `a` falls back to its default value `1`.
- Property `b` is provided as `{}`. Since `b` exists, the default block `{ c: 2 }` is ignored. Destructuring retrieves `b.c`, which is `undefined` on `{}`.

> 💡 **Interviewer Focus:** Parameter destructuring default assignment boundaries.

</details>

<hr/>

### ❓ Q84. **What is the output of this asynchronous generator loop evaluation?**

```javascript
async function* getVals() {
  yield Promise.resolve(1);
  yield 2;
}

(async () => {
  for await (const val of getVals()) {
    console.log(val);
  }
})();
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
1
2
```

**Explanation:**
- An async generator yields promises or values.
- The `for-await-of` loop automatically resolves yielded promises before returning values to the loop body, logging `1` and `2`.

> 💡 **Interviewer Focus:** Asynchronous iterator loops.

</details>

<hr/>

### ❓ Q85. **Explain the output of this custom iterator implementation on a plain object.**

```javascript
const obj = {
  start: 1,
  end: 3,
  [Symbol.iterator]() {
    let current = this.start;
    let last = this.end;
    return {
      next() {
        if (current <= last) {
          return { value: current++, done: false };
        }
        return { done: true };
      }
    };
  }
};
console.log([...obj]);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
[1, 2, 3]
```

**Explanation:**
- Plain objects are not iterable by default.
- Adding the `[Symbol.iterator]` method returning a custom iterator protocol (implementing a `.next()` method returning `{ value, done }`) makes the object iterable, allowing spread operations (`[...obj]`) or `for...of` loops.

> 💡 **Interviewer Focus:** Custom iteration protocols.

</details>

<hr/>

### ❓ Q86. **What is the output of this Promise.all fail-fast sequence?**

```javascript
Promise.all([
  Promise.resolve(1),
  Promise.reject(2),
  Promise.resolve(3)
]).catch(x => console.log("Rejected:", x));
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
"Rejected: 2"
```

**Explanation:**
- `Promise.all` has **fail-fast** behavior. If any promise in the array rejects, the entire `Promise.all` immediately rejects with that error, ignoring other successful resolutions.

> 💡 **Interviewer Focus:** Promise combinator failure semantics.

</details>

<hr/>

### ❓ Q87. **Explain the output of this script execution containing overlapping function declarations and variable hoisting:**

```javascript
var a = 1;
function a() {}
console.log(typeof a);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
"number"
```

**Explanation:**
1. **Compilation Phase:** The function declaration `function a() {}` is hoisted first. Variable declaration `var a;` is ignored because the identifier `a` is already occupied by the function in scope.
2. **Execution Phase:** The assignment `a = 1` executes. This overwrites the function binding with the numeric value `1`.
3. Therefore, `typeof a` returns `"number"`.

> 💡 **Interviewer Focus:** Function hoisting priority over variable declaration, and assignment overrides.

</details>

<hr/>

### ❓ Q88. **What is the output of this code snippet executing prototype chain pollution?**

```javascript
const user = {};
user.__proto__.admin = true;

const guest = {};
console.log(guest.admin);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
true
```

**Explanation:**
- Accessing `user.__proto__` points to `Object.prototype` (the shared base prototype of all plain objects).
- Writing `user.__proto__.admin = true` pollutes the shared prototype.
- Since `guest` inherits from `Object.prototype`, it automatically retrieves the `admin` property value, returning `true` (Prototype Pollution vulnerability).

> 💡 **Interviewer Focus:** Prototype pollution security risks.

</details>

<hr/>

### ❓ Q89. **Explain what happens when a Proxy gets revoked using `Proxy.revocable()`.**

```javascript
const target = { a: 1 };
const { proxy, revoke } = Proxy.revocable(target, {});

console.log(proxy.a);
revoke();
console.log(proxy.a);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
1
TypeError: Cannot perform 'get' on a proxy that has been revoked
```

**Explanation:**
- `Proxy.revocable` returns a proxy and a `revoke` function.
- Once `revoke()` is called, the proxy is disconnected from the target object. Any subsequent attempts to access or modify properties on the proxy throw a `TypeError`.

> 💡 **Interviewer Focus:** Revocable proxy patterns for temporary resource access.

</details>

<hr/>

### ❓ Q90. **Identify the output of this complex async queue execution:**

```javascript
const p = Promise.resolve();
p.then(() => console.log("then1"));
p.then(() => console.log("then2"));
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
then1
then2
```

**Explanation:**
- Multiple `.then()` listeners attached to the *same* resolved promise are enqueued onto the microtask queue sequentially. They execute in the order they were registered.

> 💡 **Interviewer Focus:** Promise listener chaining.

</details>

<hr/>

### ❓ Q91. **What is logged here?**

```javascript
const obj = {
  get [Symbol.toStringTag]() {
    return "CustomObject";
  }
};
console.log(Object.prototype.toString.call(obj));
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
"[object CustomObject]"
```

**Explanation:**
- `Object.prototype.toString` checks for a special Symbol property `Symbol.toStringTag` on the target object.
- If present, it uses the returned string value as the class tag, resulting in `"[object CustomObject]"` instead of the standard `"[object Object]"`.

> 💡 **Interviewer Focus:** Overriding base object tagging strings.

</details>

<hr/>

### ❓ Q92. **How does JavaScript handle function overloading internally?**

<details>
<summary><b>👀 Show Answer</b></summary>

JavaScript does **not** support function overloading in its compile-time definition. If multiple functions share the same name, the last declaration overwrites prior ones.
- **Internal Resolution:** Developers implement overloading at runtime by writing checking logic inside the function using parameters verification:
  - Checking `arguments.length`.
  - Checking parameters types (`typeof arg === 'string'`).

> 💡 **Interviewer Focus:** Implementing dynamic runtime dispatch checks.

</details>

<hr/>

### ❓ Q93. **What is the output of this code using WeakRef variables?**

```javascript
let obj = { value: 42 };
const ref = new WeakRef(obj);

obj = null;
// Assume garbage collection runs here
console.log(ref.deref()?.value);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
undefined (if collected, otherwise 42)
```

**Explanation:**
- `WeakRef` creates a weak reference to the target object.
- If `obj = null` eliminates the only strong reference, the object can be garbage collected.
- Calling `.deref()` returns the target object if it is still in memory, or `undefined` if it has been garbage collected.

> 💡 **Interviewer Focus:** Weak references management.

</details>

<hr/>

### ❓ Q94. **Identify the output of this array sorting process:**

```javascript
const arr = [1, 5, 20, 10];
arr.sort();
console.log(arr);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
[1, 10, 20, 5]
```

**Explanation:**
- By default, `Array.prototype.sort()` converts elements to strings and compares their UTF-16 code units (lexicographical sorting).
- `"10"` starts with `"1"` which comes before `"5"`, resulting in the sorted sequence `[1, 10, 20, 5]`.
- **Solution:** Pass a custom comparator function: `arr.sort((a, b) => a - b)`.

> 💡 **Interviewer Focus:** Default lexicographical sorting quirks in JS arrays.

</details>

<hr/>

### ❓ Q95. **Explain what happens when we use new on an arrow function.**

```javascript
const Foo = () => {};
new Foo();
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
TypeError: Foo is not a constructor
```

**Explanation:**
- Arrow functions do **not** have their own `this` context, a prototype property, or an internal `[[Construct]]` method.
- Therefore, they cannot be called with the `new` operator, throwing a `TypeError`.

> 💡 **Interviewer Focus:** Constructor limitations of arrow functions.

</details>

<hr/>

### ❓ Q96. **What is the output of `console.log(typeof class {})`?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
"function"
```

**Explanation:**
- JavaScript classes are syntactical sugar over standard constructor functions, returning `"function"`.

> 💡 **Interviewer Focus:** Classes as function wrappers.

</details>

<hr/>

### ❓ Q97. **Identify the output of this destructuring nested alias configuration:**

```javascript
const obj = { a: { b: 2 } };
const { a: { b: c } } = obj;
console.log(c);
console.log(b);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
2
ReferenceError: b is not defined
```

**Explanation:**
- `const { a: { b: c } } = obj` destructures `obj`.
- The nested property `b` is aliased and assigned to a new variable named `c`.
- Therefore, `c` receives the value `2`. The identifier `b` is only a matching parameter and does not become a variable, throwing a `ReferenceError` on access.

> 💡 **Interviewer Focus:** Destructuring alias bindings.

</details>

<hr/>

### ❓ Q98. **What is logged here?**

```javascript
const buffer = new ArrayBuffer(8);
const view = new Int32Array(buffer);
view[0] = 42;
console.log(view.length);
console.log(view.byteLength);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
2
8
```

**Explanation:**
- `ArrayBuffer(8)` allocates 8 bytes of raw memory.
- `Int32Array` views memory as 32-bit (4-byte) signed integers.
- The number of elements (`length`) is `8 bytes / 4 bytes = 2` elements.
- The overall buffer byte length (`byteLength`) remains `8`.

> 💡 **Interviewer Focus:** Memory array buffers configurations.

</details>

<hr/>

### ❓ Q99. **Explain the output of this generator function containing return statements:**

```javascript
function* test() {
  yield 1;
  return 2;
  yield 3;
}
const t = test();
console.log(t.next().value);
console.log(t.next().value);
console.log(t.next().value);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
1
2
undefined
```

**Explanation:**
- The first `.next()` executes to the `yield 1` statement, returning `1`.
- The second `.next()` hits the `return 2` statement. This terminates the generator with state `done: true` and returns `2`.
- Any subsequent yield statements are unreachable. The third `.next()` returns `undefined`.

> 💡 **Interviewer Focus:** Generator termination on return.

</details>

<hr/>

### ❓ Q100. **Identify what is logged:**

```javascript
let obj = {
  valueOf() { return 2; },
  toString() { return "3"; }
};
console.log(obj + 1);
```

<details>
<summary><b>👀 Show Answer</b></summary>

**Output:**
```text
3
```

**Explanation:**
- The `+` operator triggers primitive coercion.
- When performing numeric arithmetic or generic additions on objects, JavaScript checks for `valueOf()` first.
- Since `valueOf()` returns `2` (a primitive number), the coercion resolves to `2 + 1 = 3`.
- If `valueOf()` were missing or returned an object, it would fall back to `toString()`.

> 💡 **Interviewer Focus:** Object-to-primitive valueOf/toString precedence rules.

</details>

<hr/>

### 🧭 Navigation

| ⬅️ Previous | 🏠 Index | ➡️ Next |
| :--- | :---: | ---: |
| [⬅️ DevOps](./11_DevOps.md) | [Home](./00_Index.md) | 🚫 *None* |
