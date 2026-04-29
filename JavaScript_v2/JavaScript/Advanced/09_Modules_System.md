# 📌 09 — Modules System

## 🧠 Concept Explanation (Deep Technical Narrative)

JavaScript has three module systems that coexist in production:
1. **CommonJS (CJS)** — Node.js original: synchronous, `require()`/`module.exports`
2. **ESM (ES Modules)** — Spec-standardized: asynchronous-capable, `import`/`export`, live bindings
3. **AMD/UMD** — Browser-targeted pre-ESM formats (legacy)

Understanding the **loader internals**, **circular dependency resolution**, and **live binding mechanics** is essential for debugging module-related production issues.

## 🔬 Internal Mechanics (Engine-Level)

### ESM Module Graph Loading (V8 + Host)

ESM loading has three distinct phases:

**Phase 1 — Construction (Parse):**
V8 parses all module source files, identifies `import` declarations, and builds the **Module Graph** (a DAG). This is recursive and synchronous in terms of graph building.

```
import './a.js'   → parse a.js → find its imports → parse those
import './b.js'   → parse b.js → ...
```

**Phase 2 — Linking (Instantiation):**
V8 creates the `ModuleEnvironmentRecord` for each module and links live bindings. At this point, imported names are bound to the **exporting module's environment record** — even though values aren't set yet.

```
// a.js exports 'x'
// b.js imports 'x' from 'a.js'
// After linking: b.js's 'x' binding points into a.js's env record slot
// Value in slot: undefined (not yet evaluated)
```

**Phase 3 — Evaluation (Execution):**
Modules execute in **post-order depth-first** (leaves first, root last). By the time a module executes, all its dependencies have already executed.

### CJS vs ESM: The Fundamental Difference

```
CJS (require):
  - Synchronous: require() BLOCKS until the module is loaded
  - Cached: second require() returns cached module.exports
  - Live copy of exports object at require time
  - Circular deps: partially evaluated module (whatever is exported so far)

ESM (import):
  - Parsed before execution (static analysis possible)
  - Live bindings: import sees current value, even if exporting module updates later
  - Circular deps: binding exists, value is TDZ until exporting module evaluates
  - Top-level await: module graph evaluation can be async
```

### Live Bindings — The Key ESM Feature

```javascript
// counter.js (ESM)
export let count = 0
export function increment() { count++ }
export function getCount() { return count }

// consumer.js
import { count, increment } from './counter.js'

console.log(count)  // 0
increment()
console.log(count)  // 1 — LIVE BINDING: sees updated value!

// CJS equivalent would NOT see the update:
// const { count } = require('./counter')  // count = 0 (copy!)
// increment()
// console.log(count)  // 0 — stale!
```

### Module Specifier Resolution (Node.js)

```
require('lodash') → algorithm:
1. If core module → return immediately
2. If starts with './' or '/' → file resolution
3. Otherwise → node_modules lookup:
   a. Check ./node_modules/lodash
   b. Check ../node_modules/lodash
   c. Check ../../node_modules/lodash
   ... up to filesystem root

ESM import specifier types:
- Relative: './foo.js' (must include extension!)
- Bare: 'lodash' (requires importmap or bundler)
- URL: 'https://example.com/module.js' (browsers)
- Data: 'data:text/javascript,...' (browsers)
```

---

## 🔁 Execution Flow — Circular Dependency

```javascript
// Circular dep: a.js imports from b.js, b.js imports from a.js

// a.js
import { valueFromB } from './b.js'
export const valueFromA = 'A'
console.log('a sees b:', valueFromB)  // What is this?

// b.js
import { valueFromA } from './a.js'
export const valueFromB = 'B'
console.log('b sees a:', valueFromA)  // What is this?
```

**ESM execution order (post-order DFS):**
```
1. Construction: parse a.js → finds b.js → parse b.js → finds a.js (cycle detected)
2. Linking: 
   - a.js's env record created: { valueFromA: TheHole }
   - b.js's env record created: { valueFromB: TheHole }
   - b.js's `valueFromA` binding → points to a.js's { valueFromA } slot
   - a.js's `valueFromB` binding → points to b.js's { valueFromB } slot

3. Evaluation (b.js first — it's the leaf):
   - b.js runs:
     - `valueFromA` is TDZ at this point (a.js not yet evaluated)
     - `export const valueFromB = 'B'` → b.js slot[valueFromB] = 'B'
     - console.log('b sees a:', valueFromA)  → TDZ ReferenceError!
     
   Actually: b sees 'undefined' in non-strict old implementations
   Or: TDZ ReferenceError in strict mode ESM (module is always strict)
```

**The fix for circular deps:**
- Use functions (evaluated at call time, not at module load time)
- Restructure to remove the circle
- Accept that initialization order matters

---

## 🧠 Memory Behavior

```
Module caching (both CJS and ESM):

CJS module cache: require.cache
  { '/path/to/module.js': Module { exports: {...} } }
  Each module lives forever once loaded (no eviction)
  
ESM module cache: part of the host's module map
  { specifier → ModuleRecord { environment, evaluationResult } }
  Also lives forever per agent (per realm)

Memory implication:
  - Modules are NEVER garbage collected (by design)
  - Module-level variables live for the process lifetime
  - This is why "module-level state" is effectively global state
  - Large modules with large initial state can dominate heap usage
```

---

## 📐 ASCII Diagram — ESM Module Graph

```
app.js (root)
├── import './utils.js'
│       ├── import './math.js'
│       │       └── (no imports)     ← evaluated 1st
│       └── import './string.js'
│               └── (no imports)     ← evaluated 2nd
│       ← evaluated 3rd
├── import './api.js'
│       └── import './utils.js'     ← already evaluated (from cache)
│       ← evaluated 4th
└── (app.js evaluated last)
```

---

## 🔍 Code Examples

### Example 1 — CJS Circular Dependency (Partial Evaluation)

```javascript
// a.cjs
const b = require('./b.cjs')
exports.a = 'A: ' + b.b  // b.b may be undefined if b hasn't exported yet

// b.cjs
const a = require('./a.cjs')  // Gets partial a (exports so far = {})
exports.b = 'B: ' + a.a  // a.a is undefined at this point!

// Result: a.b = 'B: undefined', b.b = undefined
// CJS circular deps silently produce undefined values
```

### Example 2 — ESM Lazy Loading

```javascript
// Dynamic import() — loads module as a microtask
async function loadFeature() {
  const { default: Chart } = await import('./charts.js')
  // Module graph of charts.js is loaded, linked, evaluated
  // Returns the module's namespace object
  return new Chart(data)
}

// Conditional loading (tree-shaking friendly)
const module = await import(
  isDevelopment ? './dev-tools.js' : './prod-tools.js'
)

// V8: import() returns a Promise that resolves to the Module Namespace Object
// The namespace object has live bindings to all named exports
```

### Example 3 — Module-Level Side Effects (Anti-pattern)

```javascript
// singleton.js — module-level state
let instanceCount = 0
let sharedState = {}

export function getInstance() {
  instanceCount++
  return sharedState
}

export function getCount() { return instanceCount }

// Problems:
// 1. In tests: module cache is shared → tests contaminate each other
// 2. In SSR: module cache shared across requests → request data leaks!
// 3. Module loaded once even if imported in 100 components

// Fix for tests: jest.resetModules() before each test
// Fix for SSR: factory functions instead of module-level state
export function createInstance() {
  let state = {}
  return { getState: () => state, setState: s => { state = s } }
}
```

### Example 4 — Tree Shaking Requirements

```javascript
// For tree shaking to work: named exports, no side effects

// tree-shakeable:
export function a() { return 1 }  // Only used exports are bundled
export function b() { return 2 }  // Unused: removed by bundler

// NOT tree-shakeable:
export default {  // Default export: bundler can't determine which props are used
  a: () => 1,
  b: () => 2
}

// sideEffects in package.json:
// { "sideEffects": false }  → bundler knows: safe to tree-shake everything
// { "sideEffects": ["./polyfills.js"] }  → only polyfills.js has side effects
```

---

## 💥 Production Failures

### Failure 1 — ESM/CJS Interop in Node.js

```javascript
// package.json: "type": "module"
// All .js files are treated as ESM

// WRONG: Using require() in ESM
import createRequire from 'module'
const require = createRequire(import.meta.url)
const lodash = require('lodash')  // Works but defeats ESM benefits

// WRONG: Using __dirname in ESM
console.log(__dirname)  // ReferenceError: __dirname is not defined in ESM!

// ESM equivalent:
import { fileURLToPath } from 'url'
import { dirname } from 'path'
const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)
```

### Failure 2 — SSR Module State Leakage

```javascript
// DANGEROUS: module-level state in Next.js API route (SSR)
// request-handler.js
let currentUser = null  // SHARED ACROSS ALL REQUESTS!

export default function handler(req, res) {
  currentUser = req.session.user  // Set for this request
  // ... async operation ...
  // By the time this runs, currentUser may be another request's user!
  return res.json({ user: currentUser })  // WRONG user!
}

// Fix: Use closure-scoped or request-scoped state
export default function handler(req, res) {
  const currentUser = req.session.user  // Local to this handler call
  return res.json({ user: currentUser })
}
```

---

## ⚠️ Edge Cases

### import.meta

```javascript
// Available in ESM only
import.meta.url      // Current module's URL (file:///path/to/module.js)
import.meta.resolve  // Resolve specifier relative to this module

// In browsers:
import.meta.env      // (Vite-specific) environment variables

// Node.js:
import.meta.url      // file:///Users/...
import.meta.main     // Not standard — use: process.argv[1] === fileURLToPath(import.meta.url)
```

### Named vs Default Exports and Tree Shaking

```javascript
// Named exports: tree-shakeable
export { a, b, c }
// Import only what you need:
import { a } from './module.js'  // b and c excluded from bundle

// Default + named: be careful
export default class MyClass {}
export const util = () => {}
// import MyClass from './module.js'  → util is excluded
// Works for tree shaking
```

---

## 🏢 Industry Best Practices

1. **Use ESM everywhere** — Both browser and Node.js (Node.js 12+ supports ESM natively).
2. **Mark packages with `sideEffects: false`** — Enables full tree shaking in bundlers.
3. **Avoid module-level mutable state** — Use factory functions or dependency injection.
4. **Never use circular dependencies** — Restructure to have a clear dependency direction.
5. **Use `import()` for code splitting** — Lazy-load large features only when needed.

---

## ⚖️ Trade-offs

| System | Loading | Tree-shaking | Live Bindings | Circular Deps |
|--------|---------|--------------|---------------|---------------|
| CJS | Synchronous | No | No (copies) | Partial (silent) |
| ESM | Async-capable | Yes | Yes | TDZ-safe |
| Dynamic import() | On-demand | Yes | Yes | N/A |

---

## 💼 Interview Questions (With Solutions)

**Q1: Why can't you `require()` an ESM module from CJS?**
> ESM modules must be loaded asynchronously (top-level await, async loader). CJS `require()` is synchronous — it blocks until the module is loaded. Since ESM loading can be async, there's no way to fit it into CJS's synchronous model. The fix: use dynamic `import()` in CJS code, which returns a Promise.

**Q2: How do live bindings work internally?**
> During the linking phase, ESM creates `ModuleEnvironmentRecord` for each module. Imported bindings are references (live slots) into the exporting module's env record — not copies. When the exporting module updates an exported variable, all importers immediately see the new value because they're all reading from the same memory slot (the exporting module's context slot).

**Q3: What does the module cache prevent, and when is it a problem?**
> The module cache prevents loading the same module twice, ensuring singleton behavior and saving I/O. It's a problem in: (1) tests — shared state between test suites (use `jest.resetModules()`); (2) SSR — module-level state shared across requests (restructure to factory functions); (3) hot module replacement (HMR) — stale cached modules need explicit invalidation.

---

## 🧩 Practice Problems

**Problem:** Implement a simple module loader with caching:

```javascript
class ModuleLoader {
  constructor() {
    this.cache = new Map()
    this.loading = new Map()  // In-flight deduplication
  }
  
  async load(url) {
    // Return cached
    if (this.cache.has(url)) return this.cache.get(url)
    
    // Deduplicate concurrent loads
    if (this.loading.has(url)) return this.loading.get(url)
    
    const promise = fetch(url)
      .then(r => r.text())
      .then(code => {
        // Simplified: just eval. Real loader uses VM sandbox
        const module = { exports: {} }
        new Function('module', 'exports', code)(module, module.exports)
        this.cache.set(url, module.exports)
        this.loading.delete(url)
        return module.exports
      })
    
    this.loading.set(url, promise)
    return promise
  }
  
  invalidate(url) {
    this.cache.delete(url)
  }
}
```

---

## 🔗 Navigation

**Prev:** [08_Immutability.md](08_Immutability.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [10_Proxy_and_Reflect.md](10_Proxy_and_Reflect.md)
