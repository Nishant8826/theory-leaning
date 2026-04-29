# 📌 03 — Singleton Pattern

## 🧠 Concept Explanation

The Singleton pattern ensures a class/module has only ONE instance. In Node.js, the module caching system makes this trivially achievable — every `require()` of the same module returns the same cached exports object.

However, "true" singletons can be problematic in tests (shared state between test cases) and in multi-process/multi-thread environments (each process has its own singleton).

## 🔍 Code Examples

### Module-Based Singleton (Node.js)

```javascript
// db.js — Singleton via module cache
const { Pool } = require('pg')

// This is created ONCE (module cache ensures this)
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000
})

pool.on('error', (err) => {
  console.error('Pool error:', err)
})

module.exports = pool

// Usage: require('./db') returns the SAME pool everywhere
```

### Class-Based Singleton with Lazy Initialization

```javascript
class ConfigService {
  static instance = null
  
  constructor() {
    if (ConfigService.instance) {
      return ConfigService.instance
    }
    
    this._config = null
    this._loaded = false
    ConfigService.instance = this
  }
  
  static getInstance() {
    if (!ConfigService.instance) {
      ConfigService.instance = new ConfigService()
    }
    return ConfigService.instance
  }
  
  async load() {
    if (this._loaded) return this._config
    this._config = await fetchConfig()
    this._loaded = true
    return this._config
  }
  
  get(key) {
    if (!this._loaded) throw new Error('Config not loaded')
    return this._config[key]
  }
  
  // For testing: allow reset
  static _reset() { ConfigService.instance = null }
}
```

### Singleton with Dependency Injection (Testable)

```javascript
// Instead of true singletons: use a DI container
class Container {
  constructor() {
    this.singletons = new Map()
    this.factories = new Map()
  }
  
  registerSingleton(name, factory) {
    this.factories.set(name, { factory, singleton: true })
  }
  
  registerTransient(name, factory) {
    this.factories.set(name, { factory, singleton: false })
  }
  
  resolve(name) {
    const registration = this.factories.get(name)
    if (!registration) throw new Error(`Not registered: ${name}`)
    
    if (registration.singleton) {
      if (!this.singletons.has(name)) {
        this.singletons.set(name, registration.factory(this))
      }
      return this.singletons.get(name)
    }
    
    return registration.factory(this)
  }
  
  // For tests: create a scoped container
  createScope() {
    const scope = new Container()
    scope.factories = new Map(this.factories)  // Inherit registrations
    return scope  // Fresh singleton cache
  }
}

const container = new Container()
container.registerSingleton('db', () => createDatabase())
container.registerTransient('emailService', (c) => createEmailService(c.resolve('config')))
```

## ⚠️ Singleton in Multi-Process Environments

```javascript
// WARNING: Cluster/fork creates separate processes
// Each process has its OWN singleton

cluster.fork()  // Process 1: ConfigService.instance (object A)
cluster.fork()  // Process 2: ConfigService.instance (object B) — DIFFERENT OBJECT!

// "Singleton" is per-process, not per-cluster
// For truly shared state: use Redis, database, or shared memory (SharedArrayBuffer in threads)
```

## 🏢 Industry Best Practices

1. **Prefer module cache for Node.js singletons** — Simpler and automatic.
2. **Make singletons resetable in tests** — Add `_reset()` method or use DI container.
3. **Avoid singleton for request-scoped data** — Each request needs its own state.
4. **Use DI containers** — Inversion of control makes singletons testable.

## 💼 Interview Questions

**Q1: How does Node.js module caching implement the Singleton pattern?**
> When a module is first `require()`d, Node.js evaluates it and stores the exports in `require.cache` keyed by absolute file path. Subsequent requires return the cached exports object without re-evaluating the module. This means any module-level state (variables, instances, connections) is shared across all imports of that module in the same process. `require.cache` can be manipulated for testing: `delete require.cache[require.resolve('./module')]` forces re-evaluation.

## 🔗 Navigation

**Prev:** [02_Factory_Pattern.md](02_Factory_Pattern.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [04_Observer_Pattern.md](04_Observer_Pattern.md)
