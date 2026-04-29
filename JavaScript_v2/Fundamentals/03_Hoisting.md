# 📌 03 — Hoisting

## 🧠 Concept Explanation (Deep Technical Narrative)

"Hoisting" is a programmer's mental model for what actually happens during the **binding instantiation phase** of Execution Context creation. The ECMAScript specification never uses the word "hoisting" — it describes a multi-pass initialization process where bindings are established before code executes.

Understanding hoisting requires understanding three distinct behaviors that V8 implements during EC creation:

1. **`var` declarations:** The binding is created in the VariableEnvironment and initialized to `undefined`. The assignment happens at the declaration line during execution.

2. **`function` declarations:** The binding is created AND initialized with the fully-constructed function object. The function is usable from the very first line of the scope.

3. **`let`/`const` declarations:** The binding is created but left **uninitialized**. Accessing it before the declaration line triggers a TDZ (Temporal Dead Zone) ReferenceError.

4. **`class` declarations:** Like `let`/`const` — binding created, left uninitialized, TDZ applies.

The reason these behaviors differ is **intentional language design**: function hoisting enables mutually recursive functions at the top level; `var` hoisting was a simplification that proved error-prone; TDZ was introduced with ES6 to catch initialization-order bugs at runtime rather than silently giving `undefined`.

---

## 🏗️ Common Mental Model vs Actual Behavior

**Common model:** "Variables are moved to the top of their scope."

**Actual:** Nothing moves. The parser/interpreter makes a **pre-pass** over the scope, identifying all declarations and establishing bindings in the Environment Record. The *source code* stays exactly where it is. Only the binding initialization status changes — and it differs by declaration type.

This is why the "hoisting" mental model causes confusion: it implies `var x = 5` becomes two separate `var x; x = 5` lines — which is accurate for the binding model but misleading about what V8 actually does (static analysis, not text transformation).

---

## 🔬 Internal Mechanics (Engine-Level — V8)

### V8's Two-Pass Scope Analysis

**Pass 1 — Parse and scope analysis:**
V8's parser identifies all declarations while building the AST. For each function/script scope, the scope analyzer builds a **scope object** with:
- A list of all declared variables (name, declaration type)
- Whether each variable is captured by a closure
- Whether `eval` or `with` is present (disables static analysis)

This happens at parse time — before any bytecode is generated.

**Pass 2 — Bytecode generation (Ignition):**
For each function, Ignition generates a `CreateFunctionContext` instruction that allocates the Context object with slots for all captured variables. Then for each `var` declaration, it emits a `LdaUndefined; Star <slot>` sequence. For `function` declarations, it emits code to create the function object and store it in the slot. `let`/`const` slots are left uninitialized — accessing them generates a `ThrowReferenceErrorIfHole` check.

```
// Source:
function scope() {
  console.log(x)  // undefined
  var x = 5
  console.log(y)  // ReferenceError
  let y = 10
}

// Ignition bytecode (conceptual):
CreateFunctionContext [x (var), y (let/const)]
// x slot: LdaUndefined → Store  (initialized to undefined)
// y slot: TheHole       → Store  (marked as uninitialized)
LdaGlobal console
CallProperty [log, x_slot]   ← x_slot = undefined
LdaUndefined
Star [x_slot]                ← var declaration: no-op (already undefined)
// Execution reaches let y:
ThrowIfHole [y_slot]         ← TDZ check
CallProperty [log, y_slot]   ← Never reached
LdaSmi 10
Star [y_slot]                ← let initialization
```

### The "Hole" Sentinel Value

V8 uses a special internal value called **the hole** (`v8::internal::Heap::the_hole_value`) to mark uninitialized `let`/`const` bindings. It is NOT JavaScript's `undefined` — it is a V8-internal sentinel that:
- Causes `ThrowReferenceErrorIfHole` to fire
- Cannot be observed from JavaScript directly
- Occupies the same slot size as any other value

This is why TDZ errors give "Cannot access 'x' before initialization" rather than a generic ReferenceError — V8 knows the specific slot contains the hole.

---

## 🔁 Execution Flow (Step-by-Step)

```javascript
function example() {
  foo()             // Works — function hoisted
  console.log(bar)  // undefined — var hoisted but not initialized
  console.log(baz)  // ReferenceError — TDZ
  
  function foo() { return 'hoisted function' }
  var bar = 'bar'
  let baz = 'baz'
}
```

**EC Creation Phase:**
```
1. Scan scope for declarations:
   - foo: function declaration → allocate slot, create JSFunction, store it
   - bar: var declaration → allocate slot, store undefined
   - baz: let declaration → allocate slot, store TheHole (uninitialized)
```

**EC Execution Phase:**
```
Line 1: foo() → lookup foo in LE → JSFunction found → call it ✓
Line 2: console.log(bar) → lookup bar → undefined (var was initialized to undefined) → logs "undefined"
Line 3: console.log(baz) → lookup baz → TheHole → ThrowReferenceErrorIfHole fires → ReferenceError ✗
Line 5: (function foo definition) → skipped at runtime (already processed in creation phase)
Line 6: bar = 'bar' → writes 'bar' to bar slot
Line 7: baz = 'baz' → initializes baz slot (TheHole → 'baz')
```

---

## 🧠 Memory Behavior

```
CREATION PHASE (Environment Record state):
┌─────────────────────────────────────────┐
│  foo    │  [JSFunction object ptr]       │ ← Fully initialized
│  bar    │  undefined                     │ ← Initialized to undefined
│  baz    │  TheHole (0x1)                 │ ← Uninitialized sentinel
└─────────────────────────────────────────┘

AFTER var declaration line executes:
│  bar    │  'bar' (HeapString ptr)        │ ← Assigned

AFTER let declaration line executes:
│  baz    │  'baz' (HeapString ptr)        │ ← TDZ lifted
```

**Memory cost of function hoisting:** Each hoisted function creates a `JSFunction` object on the heap during the creation phase. For a module with 100 exported functions, all 100 JSFunction objects are created when the module loads — even if only 2 are ever called. This is one reason large modules have higher initial memory footprint.

---

## 📐 ASCII Diagram — Hoisting Timeline

```
                PARSE TIME                    EXECUTION TIME
                ──────────                    ──────────────
                                              
function foo()  ┌──────────┐  foo slot ──→   foo() ✓
                │ JSFunction│  initialized
                └──────────┘
                                              
var bar = 1     ┌──────────┐  bar slot ──→   bar = undefined → bar = 1
                │ undefined │  initialized
                └──────────┘
                                              
let baz = 2     ┌──────────┐  baz slot ──→   ReferenceError → baz = 2
                │  TheHole  │  UNINITIALIZED
                └──────────┘

class Cls {}    ┌──────────┐  Cls slot ──→   ReferenceError → Cls = class
                │  TheHole  │  UNINITIALIZED
                └──────────┘
```

---

## 🔍 Code Examples

### Example 1 — Function Declaration vs Function Expression Hoisting

```javascript
// Function declarations: fully hoisted
console.log(typeof declared)    // "function"
function declared() {}

// Function expressions assigned to var: var hoisted, function NOT
console.log(typeof exprVar)     // "undefined" (var slot = undefined)
var exprVar = function() {}

// Function expressions assigned to let/const: TDZ
console.log(typeof exprLet)     // ReferenceError
let exprLet = function() {}
```

### Example 2 — Hoisting in Block Scope (Subtle)

```javascript
{
  // Block scope in strict mode
  var x = 1     // x goes to FUNCTION scope (or global), not block scope
  let y = 2     // y is block-scoped
  function z() {} // function declarations in blocks: IMPLEMENTATION DEFINED!
}

// function declaration hoisting inside blocks is one of the most
// spec-ambiguous areas in JavaScript.
// Non-strict mode (legacy): function z MAY be hoisted to outer scope
// Strict mode: function z is block-scoped
// V8 behavior in non-strict mode (quirk):
{
  console.log(typeof hoisted) // "undefined" — var-like hoisting for function name
  function hoisted() { return 1 }
  console.log(typeof hoisted) // "function"
}
console.log(typeof hoisted) // "function" — escaped block scope in non-strict!
```

### Example 3 — Class Hoisting Trap

```javascript
// Common trap: trying to use class before definition
const instance = new MyClass() // ReferenceError: Cannot access 'MyClass' before initialization

class MyClass {
  constructor() { this.value = 42 }
}

// WHY: class declarations have TDZ (same as let/const)
// Classes were deliberately designed this way — they require
// the extends clause (if any) to be evaluated first, and that
// evaluation could fail. Allowing pre-initialization access
// would create uninitialized-prototype issues.
```

### Example 4 — Hoisting Across Named Function Expressions

```javascript
var f = function factorial(n) {
  if (n <= 1) return 1
  return n * factorial(n - 1) // 'factorial' is accessible here
}

// f is accessible in outer scope
// factorial is ONLY accessible inside the function body
// It's in the function's own scope, not the outer scope

console.log(typeof f)         // "function"
console.log(typeof factorial) // "undefined" — NOT hoisted to outer scope
```

---

## 💥 Production Failures & Debugging

### Failure 1 — Async Module Initialization Order

```javascript
// utils.js
export const processData = (data) => transformer(data) // Uses transformer

// transformer.js
import { processData } from './utils.js'
export const transformer = (x) => x.map(...)

// utils.js imports transformer via circular dep
// ESM hoists BINDINGS but not values
// When utils.js first executes, transformer is TheHole (TDZ for ESM live bindings)
// processData works at CALL TIME because by then transformer is initialized
// But if processData is called during module initialization: ReferenceError

// Real incident: A utility function was called at module load time
// (for initial state) before the circular dependency completed loading
// Result: TDZ error in production but not development (different bundle order)
```

### Failure 2 — `var` in Loop with Async

```javascript
// Classic hoisting+async bug
for (var i = 0; i < 3; i++) {
  fetch(`/api/${i}`).then(res => console.log(i))
  // By the time .then() runs, loop is done: i === 3
  // Prints: 3, 3, 3
}

// Production impact: API calls made with correct path (i was 0,1,2 at fetch time)
// but all responses are processed thinking i === 3
// Can cause incorrect data mapping, wrong UI state

// Fix: let (new binding per iteration) or closure
for (let i = 0; i < 3; i++) {
  fetch(`/api/${i}`).then(res => console.log(i)) // 0, 1, 2 ✓
}
```

### Debugging TDZ errors

```javascript
// TDZ error gives: "Cannot access 'x' before initialization"
// NOT "x is not defined" (which is undeclared variable)

// To distinguish:
// "Cannot access 'x' before initialization" → TDZ, binding exists
// "x is not defined" → no binding at all in any scope

// DevTools: The stack trace will point to the line where the TDZ
// access occurs. Look BELOW that line for the actual let/const declaration.
```

---

## ⚠️ Edge Cases & Undefined Behaviors

### Parameter Scope vs Body Scope

```javascript
// Parameters have their OWN scope (parameter scope)
// Body scope is a child of parameter scope

function confusing(x = () => a, a = 1) {
  // x's default sees 'a' from parameter scope
  // at the time x is evaluated, a may be uninitialized
  let a = 2  // This 'a' is in BODY scope, shadows parameter 'a'
  return x() // x captures parameter scope 'a' (=1), not body scope 'a' (=2)
}
confusing() // Returns 1, not 2

// V8 creates a hidden parameter scope EC between outer and body EC
// This is one of the most obscure EC behaviors in the spec
```

### `typeof` and TDZ — Browser Inconsistencies (Historical)

```javascript
// In very old Firefox (pre-ES6 implementations):
// typeof x would return "undefined" even for TDZ variables
// In modern V8/SpiderMonkey: typeof x throws for TDZ

// This caused polyfills written for old browsers to silently fail
// when migrated to strict-mode ES6 modules
```

---

## 🏢 Industry Best Practices

1. **Always declare before use** — Even though `var` hoisting allows use-before-declare, it's a code smell. ESLint's `no-use-before-define` rule enforces this.

2. **Prefer `const` → `let` → avoid `var`** — `const` and `let` with TDZ catch initialization bugs at runtime; `var` silently gives `undefined`.

3. **Use ESLint's `vars-on-top`** — If legacy code requires `var`, force all declarations to the top of their scope — aligning code with its runtime behavior.

4. **Be careful with circular ESM imports** — Hoisting of ESM bindings means a circular dependency may expose a TDZ variable if the import is used during module initialization rather than at call time.

5. **Function declarations in blocks (sloppy mode)** — Never use them. Behavior is implementation-defined. Always use `const fn = function(){}` in blocks.

---

## ⚖️ Trade-offs

| Feature | Benefit | Cost |
|---------|---------|------|
| `var` hoisting | Backward compat | Silent `undefined` bugs |
| Function hoisting | Mutual recursion at module level | Eager JSFunction allocation |
| TDZ for `let`/`const` | Runtime initialization bug detection | ThrowIfHole check per access |
| `class` TDZ | Safe extends clause evaluation | Can't use class before definition |
| Parameter scope | Default parameter expressions | Hidden EC complexity |

---

## 💼 Interview Questions (With Solutions)

**Q1: What is the Temporal Dead Zone and why does it exist?**

> TDZ is the period between binding creation (EC creation phase) and binding initialization (the declaration line during execution). It exists because ES6 wanted to prevent use-before-initialization bugs that `var` allowed. The hole sentinel in V8 implements TDZ — any read from an uninitialized slot throws ReferenceError. It also exists because `class` declarations can have `extends` clauses that must be evaluated first, and allowing access before that evaluation would produce corrupted prototype chains.

**Q2: Why are function declarations fully hoisted but function expressions not?**

> Function *declarations* are syntactically a statement, and the specification requires them to be fully initialized during binding instantiation. This enables patterns like mutual recursion at the module level. Function *expressions* are expressions — they are evaluated during execution flow, not during binding setup. Only the *variable binding* (if `var`) is established during creation; the function value is created when the expression is evaluated.

**Q3: Does `typeof` bypass TDZ?**

> No — not for bindings that exist in scope. `typeof undeclaredVariable` returns `"undefined"` because there is no binding at all. `typeof tdz_variable` (where `let tdz_variable` exists later in the same scope) throws ReferenceError because the binding exists but is in TDZ. The `typeof` operator only skips the error for *completely absent* bindings, not for TDZ bindings.

---

## 🧩 Practice Problems (With Solutions)

**Problem:** What does this output and why?

```javascript
var x = 1

function outer() {
  console.log(x)  // A
  var x = 2
  
  function inner() {
    console.log(x) // B
    x = 3
  }
  
  inner()
  console.log(x)  // C
}

outer()
console.log(x)    // D
```

**Solution:**
```
A: undefined
B: 2
C: 3
D: 1

Explanation:
A: outer() creates a new VE. var x = 2 hoists x to outer's VE = undefined.
   The global x (=1) is shadowed. Log prints undefined.

B: inner() has no var x. So x lookup walks to outer's VE: x = 2 (now).

C: inner() did `x = 3` which mutates outer's x. Logs 3.

D: Global x was never mutated by inner (it mutated outer's x). Still 1.
```

---

## 🔗 Navigation

**Prev:** [02_Call_Stack.md](02_Call_Stack.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [04_Scope_and_Lexical_Environment.md](04_Scope_and_Lexical_Environment.md)
