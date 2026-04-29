# 📌 11 — Symbols & Iterators

## 🧠 Concept Explanation

`Symbol` is a primitive type introduced in ES6 — the first new primitive type since the initial spec. Symbols are:
- **Unique:** Every `Symbol()` call creates a unique value (no two are equal)
- **Non-string keys:** Can be used as property keys but won't appear in `for...in` or `Object.keys()`
- **Non-coercible:** Cannot be implicitly converted to string (explicit `.toString()` required)

**Well-known Symbols** are a set of pre-defined symbols that V8 uses to implement protocol methods — they're the bridge between JavaScript and engine internals.

The **Iterator Protocol** is defined using `Symbol.iterator` — a well-known symbol that V8 checks for to enable `for...of`, spread, destructuring, `Array.from`, etc.

## 🔬 Internal Mechanics (V8)

### Symbol Internal Representation

V8 represents Symbols as a special heap object (`JSSymbol`) with:
- A unique ID (incrementing counter per Isolate)
- An optional description string
- A flag: `is_well_known` (for built-in symbols like `Symbol.iterator`)

Symbol property keys in objects use a separate **symbol table** in the object's property storage — kept separate from string keys. This is why `Object.keys()` doesn't return symbol keys.

### Well-Known Symbols and V8 Protocol Hooks

```
Symbol.iterator    → V8 hook for for...of, spread, destructuring
Symbol.toPrimitive → V8 hook for type coercion (+, ==, template literals)
Symbol.hasInstance → V8 hook for instanceof operator
Symbol.asyncIterator → V8 hook for for await...of
Symbol.species     → V8 hook for subclass constructors in map/filter/etc
Symbol.toStringTag → V8 hook for Object.prototype.toString
Symbol.isConcatSpreadable → Array.prototype.concat behavior
```

V8 checks for these symbols at specific internal points — for example, the `for...of` loop bytecode emits `GetIterator` which specifically looks for `Symbol.iterator` on the object.

### Iterator Protocol Internal Flow

```
for (const x of iterable) { ... }

V8 bytecode:
1. GetIterator(iterable)     → calls iterable[Symbol.iterator]()
2. IteratorNext(iterator)    → calls iterator.next()
3. IteratorComplete(result)  → checks result.done
4. IteratorValue(result)     → reads result.value
5. Loop body executes with x = result.value
6. Repeat from step 2
7. IteratorClose(iterator)   → calls iterator.return() if loop exits early
```

## 🔁 Execution Flow — Custom Iterator

```javascript
class Range {
  constructor(start, end) {
    this.start = start
    this.end = end
  }
  
  [Symbol.iterator]() {
    let current = this.start
    const end = this.end
    
    return {
      next() {
        if (current <= end) {
          return { value: current++, done: false }
        }
        return { value: undefined, done: true }
      },
      return(value) {  // Called when for...of exits early
        console.log('Iterator closed early')
        return { done: true, value }
      }
    }
  }
}

for (const n of new Range(1, 5)) {
  if (n === 3) break  // Triggers iterator.return()
  console.log(n)  // 1, 2
}
```

## 🧠 Memory Behavior

```
Symbol registry (Symbol.for):
- Global symbol registry: shared across realms (unlike Symbol())
- Each Symbol.for('key') with same key returns SAME symbol
- Registry holds strong references — symbols never GC'd once registered

Iterators:
- Iterator objects (returned by [Symbol.iterator]()) are heap-allocated
- Hold reference to the iterating collection
- For...of loop: iterator created, used, then becomes eligible for GC
- Generators: heap-allocated GeneratorObject persists until done/dropped

Memory leak risk:
- Holding a reference to an iterator holds the entire source collection alive
- Async iterators: can hold network connections or file handles
```

## 📐 ASCII Diagram — Iterator Protocol

```
iterable                    iterator              consumer
    │                           │                    │
    │ [Symbol.iterator]()       │                    │
    │ ─────────────────────────►│                    │
    │                           │     next()         │
    │                           │◄───────────────────│
    │                           │  {value:1,done:F}  │
    │                           │ ──────────────────►│
    │                           │     next()         │
    │                           │◄───────────────────│
    │                           │  {value:2,done:F}  │
    │                           │ ──────────────────►│
    │                           │     next()         │
    │                           │◄───────────────────│
    │                           │  {value:U,done:T}  │
    │                           │ ──────────────────►│
```

## 🔍 Code Examples

### Example 1 — Symbol as Private-ish Keys

```javascript
// Symbols prevent accidental key collisions in mixins/frameworks
const INTERNAL_STATE = Symbol('internalState')
const CLEANUP = Symbol('cleanup')

class EventBus {
  constructor() {
    this[INTERNAL_STATE] = {
      listeners: new Map(),
      active: true
    }
  }
  
  on(event, fn) {
    const state = this[INTERNAL_STATE]
    if (!state.listeners.has(event)) state.listeners.set(event, [])
    state.listeners.get(event).push(fn)
    return () => this.off(event, fn)
  }
  
  [CLEANUP]() {
    this[INTERNAL_STATE].active = false
    this[INTERNAL_STATE].listeners.clear()
  }
}

const bus = new EventBus()
// External code cannot accidentally access INTERNAL_STATE
// (they don't have the Symbol reference)
// Object.keys(bus) → [] (symbols not included)
// JSON.stringify(bus) → {} (symbols not serialized)
```

### Example 2 — Generator as Iterator

```javascript
function* fibonacci() {
  let [prev, curr] = [0, 1]
  while (true) {
    yield curr;
    [prev, curr] = [curr, prev + curr]
  }
}

// Generator automatically implements iterator protocol
const fib = fibonacci()
console.log(fib.next())  // { value: 1, done: false }
console.log(fib.next())  // { value: 1, done: false }
console.log(fib.next())  // { value: 2, done: false }

// Works with for...of (generator has Symbol.iterator that returns itself)
for (const n of fibonacci()) {
  if (n > 100) break
  console.log(n)
}

// Take N items from generator
function take(n, iterable) {
  const result = []
  for (const value of iterable) {
    result.push(value)
    if (result.length === n) break
  }
  return result
}

take(10, fibonacci())  // [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```

### Example 3 — Async Iterator (Streaming)

```javascript
// Async iterator for paginated API
async function* fetchAllPages(url) {
  let nextUrl = url
  
  while (nextUrl) {
    const response = await fetch(nextUrl)
    const data = await response.json()
    
    yield* data.items  // Yield each item from the page
    
    nextUrl = data.nextPageUrl || null
  }
}

// Consumer: processes items as they arrive
for await (const item of fetchAllPages('/api/items')) {
  await processItem(item)
  // No need to buffer all pages in memory
}

// Node.js streams implement async iterator:
import { createReadStream } from 'fs'
const stream = createReadStream('./large-file.json')
for await (const chunk of stream) {
  processChunk(chunk)  // Process chunk-by-chunk
}
```

### Example 4 — Symbol.toPrimitive

```javascript
class Money {
  constructor(amount, currency) {
    this.amount = amount
    this.currency = currency
  }
  
  [Symbol.toPrimitive](hint) {
    switch(hint) {
      case 'number': return this.amount
      case 'string': return `${this.amount} ${this.currency}`
      case 'default': return this.amount  // Used in + with other values
    }
  }
}

const price = new Money(42.99, 'USD')
`Price: ${price}`        // "Price: 42.99 USD" (string hint)
price + 10               // 52.99 (default → number hint)
+price                   // 42.99 (number hint)
price > 40               // true (number hint)
```

## 💥 Production Failures

### Failure — Symbol.for Across Realms

```javascript
// Symbol.for uses a GLOBAL registry shared across realms
// This makes it useful for cross-realm communication

// In iframe:
const iframeSymbol = iframe.contentWindow.Symbol.for('myapp.user')
// In main:
const mainSymbol = Symbol.for('myapp.user')

iframeSymbol === mainSymbol  // TRUE — same global registry

// Compare to Symbol():
const iframeSym = iframe.contentWindow.Symbol('key')
const mainSym = Symbol('key')
iframeSym === mainSym  // FALSE — different symbols
```

### Failure — Generator Memory Leak

```javascript
// Generators hold their internal state alive
function* generate(array) {
  for (const item of array) {
    yield processItem(item)
  }
}

const largeArray = new Array(100000).fill({})
const gen = generate(largeArray)

// If gen is kept alive but not fully consumed:
// largeArray is retained by the generator's closure
// Even if you set largeArray = null, gen still holds it

// Fix: Always close generators when done
const gen2 = generate(largeArray)
try {
  const first = gen2.next().value
  // Use first, then explicitly close
} finally {
  gen2.return()  // Closes generator, releases references
}
```

## ⚠️ Edge Cases

### Symbol.iterator on Regular Objects

```javascript
// Plain objects are NOT iterable by default
const obj = { a: 1, b: 2, c: 3 }
for (const x of obj) { ... }  // TypeError: obj is not iterable

// Make it iterable:
obj[Symbol.iterator] = function*() {
  yield* Object.values(this)
}

for (const x of obj) { console.log(x) }  // 1, 2, 3
```

## 🏢 Industry Best Practices

1. **Use Symbol.for() for shared protocol keys** — Cross-module or cross-realm symbols.
2. **Use Symbol() for instance-private keys** — Can't be accessed without the symbol reference.
3. **Implement Symbol.iterator for domain objects** — Makes them work with all iteration consumers.
4. **Always handle iterator cleanup** — Implement `return()` for async iterators that hold resources.

## 💼 Interview Questions

**Q1: What is the difference between `Symbol()` and `Symbol.for()`?**
> `Symbol()` creates a unique symbol each time — no two are equal. `Symbol.for('key')` looks up or creates a symbol in the global symbol registry, shared across all realms. The same key always returns the same symbol. Use `Symbol()` for module-internal keys (true uniqueness); use `Symbol.for()` for cross-module protocol keys.

**Q2: How does V8 use well-known symbols?**
> Well-known symbols are pre-allocated in V8's per-Isolate symbol table. V8's bytecode and runtime check for these symbols at specific points: `GetIterator` bytecode checks for `[Symbol.iterator]`, type conversion operators check `[Symbol.toPrimitive]`, `instanceof` checks `[Symbol.hasInstance]`. This is the mechanism by which JS can override engine-level behaviors.

## 🔗 Navigation

**Prev:** [10_Proxy_and_Reflect.md](10_Proxy_and_Reflect.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [12_TypedArrays_and_ArrayBuffers.md](12_TypedArrays_and_ArrayBuffers.md)
