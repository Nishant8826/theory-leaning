# 📌 05 — Strategy Pattern

## 🧠 Concept Explanation

The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable. It lets the algorithm vary independently from clients that use it. In JavaScript, strategies are simply functions or objects with a defined interface.

## 🔍 Code Examples

### Sorting Strategy

```javascript
const strategies = {
  bubble: (arr) => { /* bubble sort */ },
  quick: (arr) => { /* quicksort */ },
  merge: (arr) => { /* mergesort */ },
  built_in: (arr) => [...arr].sort()
}

class Sorter {
  constructor(strategy = 'built_in') {
    this.setStrategy(strategy)
  }
  
  setStrategy(name) {
    if (!strategies[name]) throw new Error(`Unknown strategy: ${name}`)
    this._strategy = strategies[name]
  }
  
  sort(data) { return this._strategy(data) }
}

// Dynamic strategy selection
const sorter = new Sorter()
sorter.setStrategy(data.length < 100 ? 'bubble' : 'quick')
```

### Validation Strategy

```javascript
const validators = {
  email: (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'Invalid email',
  minLength: (min) => (v) => v.length >= min || `Min ${min} chars`,
  maxLength: (max) => (v) => v.length <= max || `Max ${max} chars`,
  required: (v) => v != null && v !== '' || 'Required',
  pattern: (regex, msg) => (v) => regex.test(v) || msg
}

function validate(value, strategies) {
  for (const strategy of strategies) {
    const result = strategy(value)
    if (result !== true) return { valid: false, error: result }
  }
  return { valid: true }
}

const emailValidation = validate(email, [
  validators.required,
  validators.email,
  validators.maxLength(255)
])
```

### Payment Strategy

```javascript
class PaymentProcessor {
  constructor() {
    this.strategies = new Map()
  }
  
  register(type, strategy) {
    this.strategies.set(type, strategy)
  }
  
  async process(type, amount, details) {
    const strategy = this.strategies.get(type)
    if (!strategy) throw new Error(`Payment method not supported: ${type}`)
    return strategy.charge(amount, details)
  }
}

const processor = new PaymentProcessor()
processor.register('stripe', { charge: stripeCharge })
processor.register('paypal', { charge: paypalCharge })
processor.register('crypto', { charge: cryptoCharge })

await processor.process('stripe', 9999, cardDetails)
```

## 🏢 Industry Best Practices

1. **Use functions as strategies** — Functions are first-class objects in JS; no need for Strategy classes.
2. **Registry pattern for extensibility** — Allow registering new strategies without modifying existing code.
3. **Validate strategy existence** — Fail fast with clear error messages for unknown strategies.
4. **Document strategy interface** — TypeScript interfaces or JSDoc for strategy contracts.

## 💼 Interview Questions

**Q1: How does the Strategy pattern relate to functional programming?**
> Strategy pattern in functional terms is simply higher-order functions: passing a function (strategy) as a parameter. `array.sort(compareFn)` is the Strategy pattern — sort is the context, compareFn is the strategy. This demonstrates how design patterns from OOP are often built into the language in functional styles.

## 🔗 Navigation

**Prev:** [04_Observer_Pattern.md](04_Observer_Pattern.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [06_Middleware_Pattern.md](06_Middleware_Pattern.md)
