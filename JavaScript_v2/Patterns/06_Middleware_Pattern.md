# 📌 06 — Middleware Pattern

## 🧠 Concept Explanation

(Covered in depth in NodeJS/06_Middleware_Design.md)

The Middleware Pattern is a pipeline of processing steps where each step can: process input, call the next step, process the output. This applies beyond HTTP servers — it's used in Redux middleware, GraphQL resolvers, validation pipelines, and more.

## 🔍 Code Examples

### Redux Middleware

```javascript
// Redux middleware signature: store => next => action => result
const logger = (store) => (next) => (action) => {
  console.group(action.type)
  console.log('Dispatching:', action)
  const result = next(action)  // Call next middleware
  console.log('New state:', store.getState())
  console.groupEnd()
  return result
}

const thunk = (store) => (next) => (action) => {
  if (typeof action === 'function') {
    // Thunks: pass dispatch and getState to the function
    return action(store.dispatch, store.getState)
  }
  return next(action)
}

const applyMiddleware = (...middlewares) => (createStore) => (...args) => {
  const store = createStore(...args)
  let dispatch = store.dispatch
  
  const chain = middlewares.map(m => m(store))
  dispatch = chain.reduceRight((next, middleware) => middleware(next), dispatch)
  
  return { ...store, dispatch }
}
```

### Generic Pipeline

```javascript
class Pipeline {
  constructor() {
    this.stages = []
  }
  
  use(fn) {
    this.stages.push(fn)
    return this
  }
  
  async execute(context) {
    const execute = (index) => {
      if (index >= this.stages.length) return context
      return this.stages[index](context, () => execute(index + 1))
    }
    return execute(0)
  }
}

const orderPipeline = new Pipeline()
  .use(validateOrder)
  .use(checkInventory)
  .use(applyDiscounts)
  .use(chargePayment)
  .use(sendConfirmation)

await orderPipeline.execute({ order: newOrder })
```

## 🔗 Navigation

**Prev:** [05_Strategy_Pattern.md](05_Strategy_Pattern.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [07_Reactive_Patterns.md](07_Reactive_Patterns.md)
