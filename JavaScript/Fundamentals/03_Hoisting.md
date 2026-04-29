# 📌 03 — Hoisting

## 🌟 Introduction

**Hoisting** is one of the most misunderstood concepts in JavaScript. Many people think JavaScript "moves" code to the top, but that's not true.

Hoisting is a behavior where you can access variables and functions **before** they are initialized in the code. It is a direct result of how the **Execution Context** is created.

---

## 🏗️ How it Works (The "Pre-Scan")

Remember the **Two Phases** of Execution Context?
1.  **Creation Phase:** The engine scans your code for declarations and sets aside memory.
2.  **Execution Phase:** The engine runs your code line-by-line.

Because memory is allocated **before** the code runs, the engine "knows" about your variables and functions ahead of time. This is what we call Hoisting.

---

## 🔄 Hoisting by Declaration Type

| Type | Hoisted? | Initial Value | Access before declaration? |
| :--- | :--- | :--- | :--- |
| **Function** | ✅ Yes | Actual Function | ✅ Works (Full Hoisting) |
| **`var`** | ✅ Yes | `undefined` | ✅ Returns `undefined` |
| **`let` / `const`**| ✅ Yes | < Uninitialized > | ❌ Error (ReferenceError) |

---

## 📐 Visualizing the Hoisting "Memory Pass"

The JS engine doesn't move code; it just populates a "Memory Record" before execution.

```text
 SOURCE CODE (Script.js)            MEMORY RECORD (Creation Phase)
 ───────────────────────            ──────────────────────────────
 1. console.log(a);                 [ a      : undefined ]
 2. var a = 10;                     [ greet  : fn { ... } ]
 3. greet();                        [ b      : <the hole> ]
 4. function greet() { ... }
 5. let b = 20;
 
 EXECUTION PHASE:
 1. console.log(a)  ──▶ Looks at Memory Record ──▶ Finds 'undefined' ──▶ Logs 'undefined'
 2. a = 10          ──▶ Updates Memory Record  ──▶ [ a : 10 ]
 3. greet()         ──▶ Looks at Memory Record ──▶ Finds 'fn' ──▶ Executes it!
 4. let b = 20      ──▶ Removes from "The Hole" ──▶ [ b : 20 ]
```

---

## 🛠️ Real-World Troubleshooting (Q&A)

**P1: "Function is not a function" error.**
> **Problem:** `myFunc();` results in `TypeError: myFunc is not a function`.
> **Reason:** You are using a **Function Expression** with `var`. 
> `var myFunc = function() { ... }` is hoisted as `undefined`. You are basically trying to call `undefined()`.
> **Fix:** Use a Function Declaration `function myFunc() { ... }` or move the call below the expression.

**P2: TDZ errors in loops or callbacks.**
> **Problem:** `ReferenceError: Cannot access 'data' before initialization`.
> **Reason:** You are trying to use a `let/const` variable inside a function that is called *before* the variable is defined in the script.
> **Fix:** Reorganize your code so that declarations always happen before usage, or use `var` (though not recommended).

**P3: Silent bugs with `var` and Global Scope.**
> **Problem:** A variable has the value `undefined` even though I thought I set it.
> **Reason:** You might have another `var` with the same name in a different part of the file, and hoisting is making it difficult to track which one is being used.
> **Fix:** Stop using `var`. `let` and `const` provide "block scope" and throw errors if you mess up, making bugs much easier to find.

---

## ⚡ The Temporal Dead Zone (TDZ)

The **TDZ** is the period between the start of the block and the line where the variable is declared.

> [!IMPORTANT]
> TDZ was introduced in ES6 to help developers catch bugs early. Using a variable before defining it is usually a mistake!

---

## 🔬 Deep Technical Dive (V8 Internals)

### The "Hole"
Internally, V8 uses a special value called **The Hole** (or `hash_hole`) to mark `let` and `const` variables that are in the TDZ. When V8 tries to read a variable and finds "The Hole", it automatically throws a `ReferenceError`.

---

## 💼 Interview Questions

**Q1: Are arrow functions hoisted?**
> **Ans:** Arrow functions are usually assigned to variables. They follow the rules of the variable they are assigned to. If it's `var`, it's `undefined`. If it's `const/let`, it's in the TDZ.

**Q2: What is the difference between "undefined" and "not defined"?**
> **Ans:** `undefined` means the variable exists in memory but has no value yet. `not defined` means the engine has no record of the variable at all.

---

## ⚖️ Trade-offs

| Feature | Benefit | Cost |
| :--- | :--- | :--- |
| **Function Hoisting** | Flexibility in code organization. | Can make code harder to follow. |
| **TDZ (`let/const`)** | Catches initialization bugs. | Requires stricter code structure. |

---

## 🔗 Navigation

**Prev:** [02_Call_Stack.md](02_Call_Stack.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [04_Scope_and_Lexical_Environment.md](04_Scope_and_Lexical_Environment.md)
