# 📌 07 — Composition vs Inheritance

## 🧠 Concept Explanation

"Favor object composition over class inheritance" — Gang of Four (1994). Inheritance models "is-a" relationships and bundles state + behavior into a hierarchy. Composition models "has-a" relationships and assembles behavior from smaller, independent pieces.

JavaScript's prototype system makes both possible, but class-based deep inheritance hierarchies cause specific problems in V8: hidden class fragmentation, megamorphic method dispatch, and tight coupling that prevents optimization.

## 🔬 Internal Mechanics (V8)

### Inheritance and Hidden Class Fragmentation

```javascript
class A { constructor() { this.a = 1 } }
class B extends A { constructor() { super(); this.b = 2 } }
class C extends B { constructor() { super(); this.c = 3 } }

// Instance of C has hidden class: { a:offset0, b:offset8, c:offset16 }
// Created via transition: M0 → M1(+a) → M2(+b) → M3(+c)
// 4 hidden class objects created in Map Space

// Composition equivalent:
const withA = (base) => ({ ...base, a: 1 })
const withB = (base) => ({ ...base, b: 2 })
const withC = (base) => ({ ...base, c: 3 })
const obj = withC(withB(withA({})))
// Single flat object: { a:1, b:2, c:3 }
// Same hidden class as any { a,b,c } shaped object → monomorphic ICs
```

### Method Dispatch Cost

```javascript
// Inheritance: method found at depth 3 in prototype chain
instance.method()  // Check instance → B.proto → A.proto → Object.proto

// Composition: method is own property or directly on one object
// V8 IC caches location more efficiently for shallow chains
```

## 📐 Diagram — Inheritance vs Composition

```
INHERITANCE:
Animal
  └─ Mammal
       └─ Dog (has: breathe, run, bark)
            └─ GuideDog (has: guide)

COMPOSITION (mixins):
const GuideDog = compose(
  withBreathing,   // adds: breathe()
  withRunning,     // adds: run()
  withBarking,     // adds: bark()
  withGuiding      // adds: guide()
)({})
// Flat object, any combination possible
```

## 🔍 Code Examples

### Example 1 — Mixin Composition

```javascript
const Serializable = {
  serialize() { return JSON.stringify(this) },
  hydrate(json) { return Object.assign(Object.create(this), JSON.parse(json)) }
}

const Validatable = {
  validate() {
    return this.rules.every(rule => rule(this))
  }
}

const Persistable = {
  async save() {
    if (!this.validate()) throw new Error('Validation failed')
    return db.upsert(this.tableName, this.serialize())
  }
}

// Compose a User model
const User = Object.assign(
  Object.create(null),
  Serializable,
  Validatable,
  Persistable,
  {
    tableName: 'users',
    rules: [
      u => u.name && u.name.length > 0,
      u => u.email && u.email.includes('@')
    ],
    create(data) { return Object.assign(Object.create(User), data) }
  }
)
```

### Example 2 — Functional Composition vs Class Hierarchy

```javascript
// Anti-pattern: God Object via deep inheritance
class Vehicle {
  constructor() { this.speed = 0; this.fuel = 100 }
  accelerate(amount) { this.speed += amount }
  refuel() { this.fuel = 100 }
}

class Car extends Vehicle {
  constructor() { super(); this.wheels = 4 }
  honk() { return 'Beep!' }
}

class ElectricCar extends Car {
  constructor() { super(); this.battery = 100; this.fuel = 0 }
  // Now `fuel` is inherited but meaningless — violation of Liskov!
  refuel() { throw new Error('Electric cars cannot refuel') }
  charge() { this.battery = 100 }
}

// Better: Composition
const createElectricCar = () => ({
  speed: 0,
  battery: 100,
  wheels: 4,
  accelerate(amount) { this.speed += amount },
  honk() { return 'Beep!' },
  charge() { this.battery = 100 }
  // No fuel-related methods — no Liskov violation
})
```

## 💥 Production Failure — Inheritance Mismatch (Liskov Violation)

```javascript
// Square extends Rectangle — classic Liskov Substitution Principle violation
class Rectangle {
  setWidth(w) { this.width = w }
  setHeight(h) { this.height = h }
  area() { return this.width * this.height }
}

class Square extends Rectangle {
  setWidth(w) { this.width = this.height = w }   // Override: must set both
  setHeight(h) { this.width = this.height = h }  // Override: must set both
}

// Code that expects Rectangle behavior:
function growRectangle(r) {
  r.setWidth(10)
  r.setHeight(5)
  return r.area()
}

growRectangle(new Rectangle())  // 50 ✓
growRectangle(new Square())     // 25 ✗ — Square is NOT a proper Rectangle!
// Last setHeight(5) overrides the setWidth(10) → 5*5=25
```

## ⚠️ Edge Cases

### Mixin Collision

```javascript
const A = { greet() { return 'Hello from A' } }
const B = { greet() { return 'Hello from B' } }

const AB = Object.assign({}, A, B)
AB.greet()  // 'Hello from B' — B wins (last write)
// Silent collision! A.greet is completely overwritten
// Solution: Explicit merge strategy
const AB_safe = {
  ...A,
  ...B,
  greet() { return `${A.greet()} + ${B.greet()}` }
}
```

## 🏢 Industry Best Practices

1. **Use composition for cross-cutting concerns** — Logging, serialization, validation.
2. **Use inheritance for genuine "is-a" hierarchies** — React.Component, Error subclasses.
3. **Keep inheritance depth ≤ 2** — More than 2 levels = maintenance nightmare.
4. **Prefer interfaces/mixins over inheritance** — TypeScript interfaces enable composition contracts without hierarchy.

## 💼 Interview Questions

**Q1: Why does "composition over inheritance" matter in V8 performance terms?**
> Deep inheritance chains create long prototype chains. Each method lookup must traverse more chain links, increasing IC complexity. Flat composed objects have methods as own properties or one prototype hop — V8 can cache these more effectively as monomorphic ICs. Additionally, consistent object shapes (same properties in same order) across composed instances enable better hidden class reuse.

**Q2: What is the Fragile Base Class problem?**
> When a subclass depends on implementation details of its superclass, a change to the superclass can break the subclass in unexpected ways. The subclass is "fragile" because it's tightly coupled to the internal behavior of the base class. Composition avoids this by depending on interfaces rather than implementations.

## 🔗 Navigation

**Prev:** [06_Currying.md](06_Currying.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [08_Immutability.md](08_Immutability.md)
