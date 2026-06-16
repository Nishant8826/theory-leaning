# Modules

If you do not understand how Node.js wraps and loads code files, you will encounter bugs where variables leak into global scopes, paths fail to resolve, or circular references trigger silent `undefined` crashes. Mastery of module wrapping is key to writing modular backend systems.

### The Necessity of Modules
In standard client-side browser JavaScript (before ES Modules), script tags shared the global scope (`window`). If `script1.js` declared a variable `const db = {}`, and `script2.js` declared the same variable, it created a collision. 
A **Module System** divides an application into isolated files. Each file is a module with its own private scope. Variables and functions are inaccessible to other files unless explicitly exported.

### The Module Wrapper Function
When you run a JavaScript file in Node.js, V8 does not execute your code directly. Instead, Node.js wraps your file's code in a function. This function isolates the file's variables from the global scope.

Before compilation, Node wraps the code in the following structure:
```javascript
(function(exports, require, module, __filename, __dirname) {
  // YOUR MODULE CODE LIVES HERE
});
```

Because of this wrapper:
* Every module has its own local variables (preventing global scope pollution).
* Variables like `require` and `module` are available inside the file despite not being declared by you.

## Deep Dive

### Variables Injected by the Module Wrapper
1. **`exports`**: A reference that defaults to `module.exports`. Used to expose functions/objects from the file.
2. **`require`**: A helper function used to import modules, resolve file paths, and fetch dependencies.
3. **`module`**: A reference to the current module object itself, containing metadata (like `module.id`, `module.loaded`, and `module.exports`).
4. **`__filename`**: The absolute local filesystem path of the current code file.
5. **`__dirname`**: The absolute path of the directory containing the current code file.

### Circular Dependencies
A circular dependency occurs when Module A requires Module B, and Module B requires Module A:
```text
[ Module A ] ─── requires ───> [ Module B ]
     ▲                             │
     └───────── requires ──────────┘
```
In Node's module system, when Module B requires Module A, it receives an **incomplete copy** of Module A's exports because Module A has not finished executing. This can result in variables from Module A resolving to `undefined` inside Module B.

## Visual Explanation

### The Wrapping and Execution Flow
```text
  [ raw_code.js ]
        │
        ▼ (Wrap step)
  [ (function(exports, require, module, __filename, __dirname) { ... raw_code ... }) ]
        │
        ▼ (Pass context parameters)
  [ V8 Compiler compiles wrapping function ]
        │
        ▼ (Execute)
  [ Run with parameters bound to active file details ]
```

## Real-World Example
Consider building a modular database system. You create a helper module `db.js` that connects to the database, and an application entrypoint `app.js`. Thanks to the module wrapper, the database configurations defined in `db.js` are private, preventing other modules from accidentally overwriting the connection credentials.

## Code Examples

### Examining the Module Wrapper
We can check the parameters injected by the wrapper using standard JavaScript reflection:

```javascript
// print-wrapper-args.js

// 1. Inspect the 'arguments' object injected into the wrapping function
console.log('Total injected arguments:', arguments.length); // 5

console.log('__filename:', __filename); // Absolute path to file
console.log('__dirname :', __dirname);  // Absolute path to folder containing file

console.log('module object structure:', {
  id: module.id,
  path: module.path,
  loaded: module.loaded,
  exports: module.exports
});

// 2. Proving exports reference equality
console.log('exports is alias for module.exports:', exports === module.exports); // true

// 3. Inspecting the actual wrapper string (V8 internals helper)
const moduleSystem = require('module');
console.log('\nNode.js Wrapping code signature:');
console.log(moduleSystem.wrapper);
// Output: [ '(function (exports, require, module, __filename, __dirname) { ', '\n});' ]
```

## Best Practices
* **Do Not Assign to exports Directly**: Always use `module.exports = ...` or assign properties (e.g. `exports.myFunc = ...`). Reassigning `exports = ...` breaks the reference to `module.exports`, meaning nothing gets exported.
* **Avoid Circular References**: Design your database and model structures hierarchically to prevent circular dependencies. Use shared core modules if two modules require access to the same resources.
* **Avoid Modifying the global Object**: Avoid writing properties to `global.db` or `global.config`. Use modules and dependency injection to share instances instead.

## Interview Questions

**Q:** What is a module in Node.js and why do we use them?

> **Answer:**
> A module is an isolated JavaScript file containing code that is wrapped in its own scope. We use modules to organize codebases into maintainable files, encapsulate logic, and prevent variable collisions in the global namespace.

**Q:** Explain the Node.js Module Wrapper Function.

> **Answer:**
> Before executing a file, Node.js wraps its code in a function block: `(function(exports, require, module, __filename, __dirname) { ... })`. This isolates the file's variables from the global scope and injects variables like `require` and `module` so they are accessible inside the file.

**Q:** What is a circular dependency in Node.js, and how does the runtime handle it?

> **Answer:**
> A circular dependency occurs when Module A imports Module B, and Module B imports Module A. Node.js handles this by returning an incomplete (partial) object representation of Module A's exports to Module B. When Module B tries to access properties that Module A has not yet reached or exported, those properties return `undefined`.

**Q:** Analyze the design implications of exports being an alias of module.exports. Explain how developers break this alias, why it halts module parsing, and how to debug memory leakage in cached module instances.

> **Answer:**
> The parameter `exports` is passed as a reference to `module.exports`. If you assign properties (e.g. `exports.name = 'db'`), both point to the same object in memory. However, if you reassign `exports` (e.g. `exports = { name: 'db' }`), you rebind the local `exports` variable to a new object, leaving the original `module.exports` unchanged. As a result, the module returns its default empty object `{}`.
> 
> Because Node.js caches modules in `require.cache` after the first import, subsequent requests return the exact same instance. If a module stores user state or accumulates references inside local variables, those references are never garbage collected, leading to a memory leak. You can debug this by monitoring `require.cache` and ensuring modules remain stateless, utilizing factory functions or class instantiations to pass state when needed.

---
Previous : [08_npx.md](08_npx.md) | Index : [00_index.md](00_index.md) | Next : [10_CommonJS.md](10_CommonJS.md)
