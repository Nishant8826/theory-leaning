# 📌 02 — Factory Pattern

## 🧠 Concept Explanation

The Factory Pattern is a function that creates and returns objects without using `new` directly. It encapsulates object creation logic, allows varying the type of object created based on parameters, and avoids exposing the constructor.

Unlike classes, factories don't create prototype chains — they create plain objects (or any type), which can be faster for simple value objects and avoids `new` gotchas.

## 🔍 Code Examples

### Basic Factory

```javascript
function createUser(type, data) {
  const base = {
    id: generateId(),
    createdAt: Date.now(),
    ...data
  }
  
  switch(type) {
    case 'admin':
      return {
        ...base,
        role: 'admin',
        permissions: ['read', 'write', 'delete', 'manage'],
        canManageUsers: () => true,
        canDeleteAll: () => true
      }
    
    case 'editor':
      return {
        ...base,
        role: 'editor',
        permissions: ['read', 'write'],
        canManageUsers: () => false,
        canDeleteAll: () => false
      }
      
    case 'viewer':
      return {
        ...base,
        role: 'viewer',
        permissions: ['read'],
        canManageUsers: () => false,
        canDeleteAll: () => false
      }
      
    default:
      throw new Error(`Unknown user type: ${type}`)
  }
}
```

### Abstract Factory (Creating Related Objects)

```javascript
// Database factory: creates related query builders
function createDatabase(type) {
  if (type === 'postgres') {
    return {
      query: (sql, params) => pgPool.query(sql, params),
      transaction: async (fn) => {
        const client = await pgPool.connect()
        try {
          await client.query('BEGIN')
          await fn(client)
          await client.query('COMMIT')
        } catch(e) {
          await client.query('ROLLBACK')
          throw e
        } finally {
          client.release()
        }
      },
      createQueryBuilder: () => new PostgresQueryBuilder(),
      migrate: () => runPgMigrations()
    }
  }
  
  if (type === 'sqlite') {
    return {
      query: (sql, params) => sqliteDb.prepare(sql).all(params),
      transaction: (fn) => sqliteDb.transaction(fn)(),
      createQueryBuilder: () => new SQLiteQueryBuilder(),
      migrate: () => runSQLiteMigrations()
    }
  }
}

// Usage:
const db = createDatabase(process.env.DB_TYPE)
// All code uses the same interface regardless of underlying DB
```

### Factory with Caching/Registry

```javascript
const ServiceRegistry = (() => {
  const services = new Map()
  
  return {
    register(name, factory) {
      services.set(name, factory)
    },
    
    create(name, ...args) {
      const factory = services.get(name)
      if (!factory) throw new Error(`Service not found: ${name}`)
      return factory(...args)
    },
    
    createSingleton(name, ...args) {
      const key = `${name}:singleton`
      if (!services.has(key)) {
        services.set(key, this.create(name, ...args))
      }
      return services.get(key)
    }
  }
})()

ServiceRegistry.register('email', (config) => ({
  send: (to, subject, body) => emailAdapter.send(to, subject, body, config),
  sendBulk: (recipients, template) => emailAdapter.bulk(recipients, template, config)
}))
```

## ⚖️ Factory vs Class vs Constructor

| Aspect | Factory Function | Class | Constructor Function |
|--------|-----------------|-------|---------------------|
| `new` required | No | Yes | Yes |
| Prototype chain | No (by default) | Yes | Yes |
| Privacy | Closure | No (JS) | Closure |
| Return type | Anything | Instance | Override with object |
| Subclassing | Composition | `extends` | Prototype manipulation |

## 💼 Interview Questions

**Q1: When would you prefer a factory function over a class?**
> Factory functions are preferred when: (1) you need true private state (closure-based vs class-proposal private fields); (2) the return type may vary (e.g., different implementations based on parameters); (3) you want to avoid `new` keyword gotchas; (4) you're creating many small value objects and want to avoid prototype chain overhead; (5) you're composing behavior from multiple sources (mixins) rather than inheriting.

## 🔗 Navigation

**Prev:** [01_Module_Pattern.md](01_Module_Pattern.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [03_Singleton_Pattern.md](03_Singleton_Pattern.md)
