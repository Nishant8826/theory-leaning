# 📌 07 — Prototype & Inheritance

## 🧠 Concept Explanation (Deep Technical Narrative)

JavaScript's prototype system is a **delegation-based inheritance** model, fundamentally different from class-based inheritance. When you access a property on an object and it doesn't exist on the object itself, the engine **delegates** the lookup to the object's prototype (via the `[[Prototype]]` internal slot), then that prototype's prototype, and so on — forming the prototype chain.

This is not a copy — it is live delegation. Methods on prototypes are NOT copied to instances; they are found via chain traversal each time. This has profound implications for memory (one method definition serves all instances), performance (V8's inline caches optimize prototype lookups), and semantics (mutations to the prototype are immediately visible to all instances).

The ES6 `class` syntax is **syntactic sugar** over the prototype system — it compiles to `Object.create(Parent.prototype)` for class body setup and `[[Prototype]]` linking. There is no separate "class-based" implementation in V8.

---

## 🔬 Internal Mechanics (Engine-Level — V8)

### Hidden Classes (Maps) — The Core Optimization

Every V8 object has a **hidden class** (called a Map internally). The hidden class encodes:
- The object's shape: which properties exist and their order
- Each property's offset in the object's backing store
- The object's prototype
- The object's element kind (packed SMI array, holey array, etc.)

When properties are added to objects in a consistent order, V8 creates a **transition tree**:

```
Empty Map (M0)
     │ [add property 'x' at offset 0]
     ▼
Map M1: { x: offset 0 }
     │ [add property 'y' at offset 8]
     ▼
Map M2: { x: offset 0, y: offset 8 }
```

Objects that follow the same property-addition order share the same transition tree and end up with the same hidden class. V8's **inline caches (ICs)** cache the offset lookup keyed on the hidden class:

```
// At property access site obj.x:
IC stores: (M2 → offset 0)
Next time obj.x on a M2-shaped object: direct memory access, no lookup
```

### Property Lookup: Own vs Prototype Chain

```
V8 property lookup algorithm:

1. Check object's own properties (in-object properties first, then property array)
   → If found: return value (cache hidden class → offset in IC)
   
2. If not found: load object.[[Prototype]]
   → If null: return undefined
   → If not null: repeat from step 1 with prototype object
```

V8 can cache prototype chain lookups too — it caches the entire chain, invalidating when any object in the chain changes shape.

### Prototype Chain in Memory

```
┌──────────────────────┐
│  instance            │ ← Your object
│  Map → HiddenClass   │
│  [[Prototype]] ──────┼──────────────────────────┐
│  x: 1                │                          │
└──────────────────────┘                          │
                                                  ▼
                               ┌──────────────────────────┐
                               │  Constructor.prototype    │
                               │  [[Prototype]] ───────────┼──┐
                               │  method1: JSFunction      │  │
                               │  method2: JSFunction      │  │
                               └──────────────────────────┘  │
                                                              ▼
                                         ┌──────────────────────────┐
                                         │  Object.prototype         │
                                         │  [[Prototype]]: null      │
                                         │  hasOwnProperty: fn       │
                                         │  toString: fn             │
                                         └──────────────────────────┘
```

---

## 🔁 Execution Flow (Step-by-Step)

```javascript
class Animal {
  constructor(name) {
    this.name = name  // Own property
  }
  speak() {           // On Animal.prototype
    return `${this.name} makes a sound`
  }
}

class Dog extends Animal {
  constructor(name) {
    super(name)
    this.breed = 'Unknown'
  }
  speak() {
    return `${this.name} barks`
  }
}

const d = new Dog('Rex')
d.speak()
```

**Step-by-step property lookup for `d.speak()`:**

```
1. Check d's own properties: { name: 'Rex', breed: 'Unknown' }
   → 'speak' not found in own properties

2. Load d.[[Prototype]] → Dog.prototype
   Check Dog.prototype's own properties: { constructor, speak }
   → 'speak' FOUND → return Dog.prototype.speak

3. IC at call site now caches:
   (Dog's hidden class → Dog.prototype → speak offset)
   Next call with same-shaped Dog: direct lookup, no chain walk
```

**Compiled class desugaring:**
```javascript
// What V8 actually processes (conceptually)
function Animal(name) { this.name = name }
Animal.prototype.speak = function() { return `${this.name} makes a sound` }

function Dog(name) {
  Animal.call(this, name)  // super(name)
  this.breed = 'Unknown'
}
Object.setPrototypeOf(Dog.prototype, Animal.prototype)
Dog.prototype.speak = function() { return `${this.name} barks` }
Dog.prototype.constructor = Dog
```

---

## 🧠 Memory Behavior

```
New Dog() — what V8 allocates:

1. JSObject (instance 'd'):
   - Map pointer (hidden class tracking { name, breed })
   - In-object property slots: name, breed (if ≤ V8's in-object property limit)
   - OR property backing array (if more properties than in-object slots)
   - [[Prototype]] pointer → Dog.prototype

2. V8 in-object property optimization:
   - First N properties (N ≈ 4-8 depending on constructor analysis)
     are stored INLINE in the JSObject (no extra pointer dereference)
   - Additional properties go in a separate backing store
   - V8 analyzes constructor to predict N at class creation time

Memory per instance: ~60-100 bytes (JSObject header + in-object slots)
Memory for methods: 0 per instance (methods live on shared prototype)
```

---

## 📐 ASCII Diagram — Hidden Class Transitions

```
new Dog() — Hidden Class Transition Tree:

Map M0 (empty object)
  │ +name (offset 0)
  ▼
Map M1 { name: offset_0 }    ← after Animal constructor runs
  │ +breed (offset 8)
  ▼
Map M2 { name: offset_0, breed: offset_8 }   ← after Dog constructor runs

All Dog instances follow M0 → M1 → M2 if constructed in same order.
They ALL share Map M2 as their hidden class.

IC at 'd.speak()' call site:
  FIRST CALL: Check IC → miss → lookup chain → cache (M2 → Dog.prototype → speak_fn)
  NEXT CALLS: IC hit → Direct function call (no lookup)
```

---

## 🔍 Code Examples

### Example 1 — Hidden Class Pollution

```javascript
// V8 optimization killer: inconsistent property order
function createPoint(x, y, isSpecial) {
  const p = { x, y }
  if (isSpecial) p.z = 0  // Only some objects get `z`
  return p
}

// Half of points: Map { x, y }
// Other half: Map { x, y, z }
// Both maps exist → IC at call sites becomes bimorphic

// Code that processes these points sees mixed shapes:
function processPoints(points) {
  let sum = 0
  for (const p of points) {
    sum += p.x + p.y  // Bimorphic IC (2 shapes)
  }
}

// BETTER: Always add all properties in constructor
function createPointOptimized(x, y, isSpecial) {
  return { x, y, z: isSpecial ? 0 : undefined }
  // All objects have same shape { x, y, z }
  // z = undefined doesn't affect shape but uses same Map
  // → Monomorphic IC → fast
}
```

### Example 2 — Object.create vs class

```javascript
// Object.create: explicit prototype setup
const animalProto = {
  speak() { return `${this.name} speaks` }
}

function createAnimal(name) {
  const animal = Object.create(animalProto)
  animal.name = name
  return animal
}

// class: syntactic sugar, same prototype result
class Animal {
  constructor(name) { this.name = name }
  speak() { return `${this.name} speaks` }
}

// Memory: identical — both use prototype chain
// Performance: class syntax gets better V8 optimization hints
// (V8 knows class constructors are called with new, enables inline allocation)
```

### Example 3 — hasOwnProperty vs `in`

```javascript
const obj = Object.create({ inherited: true })
obj.own = 'yes'

// `in` walks the prototype chain
'own' in obj        // true
'inherited' in obj  // true — found on prototype
'missing' in obj    // false

// hasOwnProperty: own properties only
obj.hasOwnProperty('own')       // true
obj.hasOwnProperty('inherited') // false

// DANGER: hasOwnProperty can be overridden!
const evil = { hasOwnProperty: () => true }
evil.hasOwnProperty('anything')  // true — broken!

// Safe: Use Object.prototype.hasOwnProperty.call
Object.prototype.hasOwnProperty.call(evil, 'ownProp')  // false (correct)

// ES2022: Object.hasOwn (safe, doesn't walk chain)
Object.hasOwn(evil, 'ownProp')  // false ✓
```

### Example 4 — Mixin Pattern (Composition over Inheritance)

```javascript
// Multiple prototype chains cannot be inherited in JS
// Mixins simulate multiple inheritance via Object.assign to prototype

const Serializable = (superclass) => class extends superclass {
  serialize() { return JSON.stringify(this) }
  static deserialize(json) { return Object.assign(new this(), JSON.parse(json)) }
}

const Validatable = (superclass) => class extends superclass {
  validate() {
    return Object.keys(this).every(key => this[key] !== undefined)
  }
}

class BaseEntity {
  constructor(id) { this.id = id }
}

class User extends Serializable(Validatable(BaseEntity)) {
  constructor(id, name) {
    super(id)
    this.name = name
  }
}

// Prototype chain: User → SerializableMixin → ValidatableMixin → BaseEntity → Object
// Each mixin creates an anonymous class in the chain
// Performance: each method access may walk more chain hops
// V8 can still cache these (bimorphic or polymorphic IC)
```

---

## 💥 Production Failures & Debugging

### Failure 1 — Prototype Pollution Attack

```javascript
// Prototype pollution via deep merge (lodash < 4.17.11 had this bug)
function deepMerge(target, source) {
  for (const key of Object.keys(source)) {
    if (source[key] && typeof source[key] === 'object') {
      if (!target[key]) target[key] = {}
      deepMerge(target[key], source[key])
    } else {
      target[key] = source[key]
    }
  }
}

const maliciousInput = JSON.parse('{"__proto__": {"isAdmin": true}}')
deepMerge({}, maliciousInput)
// Now Object.prototype.isAdmin === true!
// EVERY object in the application now has isAdmin = true
// {} .isAdmin === true — authentication bypass!

// Fix: Check for '__proto__', 'constructor', 'prototype' keys
function safeMerge(target, source) {
  for (const key of Object.keys(source)) {
    if (key === '__proto__' || key === 'constructor' || key === 'prototype') {
      continue  // Skip dangerous keys
    }
    // ... rest of merge
  }
}

// Or use Object.create(null) for data objects (no prototype to pollute)
const safeObj = Object.create(null)
```

### Failure 2 — Broken instanceof After Serialization

```javascript
// Objects deserialized from JSON don't have class prototype
class Config {
  validate() { return this.version && this.settings }
}

const config = new Config()
config.version = '1.0'
config.settings = {}

const serialized = JSON.stringify(config)
const deserialized = JSON.parse(serialized)

deserialized instanceof Config  // false — plain object, not Config instance
deserialized.validate()         // TypeError: not a function

// Fix: Reviver function or factory pattern
const fixed = Object.assign(new Config(), JSON.parse(serialized))
fixed instanceof Config  // true ✓
fixed.validate()         // works ✓
```

### Debugging Prototype Chain

```javascript
// Inspect prototype chain
function protoChain(obj) {
  const chain = []
  let current = obj
  while (current !== null) {
    chain.push(
      current.constructor?.name || 
      Object.prototype.toString.call(current)
    )
    current = Object.getPrototypeOf(current)
  }
  return chain
}

protoChain(new Dog('Rex'))
// ['Dog', 'Animal', 'Object', 'null'] (conceptually)

// Chrome DevTools: right-click object in console → "Store as global variable"
// Then: Object.getPrototypeOf(temp1)
```

---

## ⚠️ Edge Cases & Undefined Behaviors

### `Object.create(null)` — Objects with No Prototype

```javascript
const pure = Object.create(null)
pure.key = 'value'

// No prototype chain at all
Object.getPrototypeOf(pure) // null

pure.toString    // undefined — no Object.prototype methods!
pure.hasOwnProperty // undefined
'key' in pure    // true (in still works — checks own properties)

// Use case: safe dictionary/hashmap (no prototype pollution risk)
// Risk: surprising behavior when code expects Object.prototype methods

// JSON.stringify works (uses its own algorithm, doesn't need toString)
JSON.stringify(pure) // '{"key":"value"}'
```

### Mutating Prototype After Creation

```javascript
const proto = { x: 1 }
const obj = Object.create(proto)

// Mutations to proto are visible immediately
proto.y = 2
obj.y  // 2 — live delegation

// But: Object.setPrototypeOf deoptimizes!
Object.setPrototypeOf(obj, {})
// V8 must invalidate ALL ICs that involve obj
// This is called a "prototype transition" and is very expensive
// V8 logs: "property access deoptimization: prototype changed"

// NEVER mutate prototype of objects that are in hot code paths
```

---

## 🏢 Industry Best Practices

1. **Maintain consistent property order in constructors** — Add all properties in the same order every time. This keeps objects on the same hidden class, enabling monomorphic ICs.

2. **Freeze shared prototypes in library code** — `Object.freeze(MyClass.prototype)` prevents accidental prototype mutations that deoptimize all instances.

3. **Use `Object.hasOwn` instead of `hasOwnProperty`** — Safer against prototype pollution attacks that override `hasOwnProperty`.

4. **Never use `Object.setPrototypeOf` on live objects** — Use it only at setup time. Use `Object.create(proto)` instead for setting prototype at creation.

5. **Prefer composition (mixins/factories) over deep inheritance chains** — Each additional level of inheritance adds a prototype chain hop per lookup and increases IC complexity.

---

## ⚖️ Trade-offs

| Design | Benefit | Cost |
|--------|---------|------|
| Prototype methods (shared) | Memory efficient | Chain lookup, IC dependency on shape |
| Instance methods (class fields) | Fastest own-property access | Per-instance function allocation |
| Deep inheritance chain | Code reuse | More chain hops, complex ICs |
| Flat composition (mixins) | Predictable lookup | Complex setup code |
| `Object.create(null)` | No prototype pollution | Loses Object.prototype methods |

---

## 💼 Interview Questions (With Solutions)

**Q1: What triggers V8 to deoptimize after a prototype chain lookup cache miss?**

> When an object's hidden class changes (property added/deleted out of expected order, `Object.setPrototypeOf` called, or `__proto__` mutated), V8 must invalidate all ICs that depend on that hidden class or prototype chain. This is called a "prototype chain invalidation." V8 marks dependent ICs for re-compilation, meaning the next execution of those code paths runs slower until new ICs are established.

**Q2: Why is `class` syntax preferred over manual prototype setup in production V8 code?**

> V8 treats `class` constructors specially: it can predict they're always called with `new` (enforced by spec), enabling pre-allocation of in-object property slots based on constructor analysis. V8 also sets up the hidden class transition tree more efficiently for class constructors. Manual prototype setup with function constructors works, but V8 gets fewer static guarantees for optimization.

**Q3: Explain how prototype pollution can bypass authentication middleware.**

> When `Object.prototype` is polluted with a property (e.g., `isAdmin: true`), every object in the runtime — including plain `{}` created for request parsing — inherits that property. Authentication middleware that checks `user.isAdmin` will find `true` even for unauthenticated users if `isAdmin` was polluted onto `Object.prototype`. The check `if (user.isAdmin)` doesn't distinguish between own properties and prototype-inherited properties.

---

## 🧩 Practice Problems (With Solutions)

**Problem:** Implement a safe deep clone that preserves prototype chain:

```javascript
function deepClone(obj, seen = new WeakMap()) {
  // Handle non-objects
  if (obj === null || typeof obj !== 'object') return obj
  
  // Handle circular references
  if (seen.has(obj)) return seen.get(obj)
  
  // Handle Date, RegExp, etc.
  if (obj instanceof Date) return new Date(obj)
  if (obj instanceof RegExp) return new RegExp(obj)
  
  // Create clone with same prototype
  const clone = Object.create(Object.getPrototypeOf(obj))
  seen.set(obj, clone)
  
  // Copy own enumerable properties
  for (const key of Object.keys(obj)) {
    clone[key] = deepClone(obj[key], seen)
  }
  
  // Copy own symbols
  for (const sym of Object.getOwnPropertySymbols(obj)) {
    if (Object.getOwnPropertyDescriptor(obj, sym).enumerable) {
      clone[sym] = deepClone(obj[sym], seen)
    }
  }
  
  return clone
}

// Test:
class Point { constructor(x,y) { this.x=x; this.y=y } }
const p = new Point(1, 2)
const clone = deepClone(p)
clone instanceof Point  // true — prototype preserved
clone === p            // false — new object
```

---

## 🔗 Navigation

**Prev:** [06_This_Keyword.md](06_This_Keyword.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [08_Event_Loop.md](08_Event_Loop.md)
