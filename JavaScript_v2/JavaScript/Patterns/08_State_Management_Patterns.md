# 📌 08 — State Management Patterns

## 🧠 Concept Explanation

State management is the discipline of controlling when, how, and where application state changes. As apps grow, ad-hoc state mutation leads to unpredictable behavior, hard-to-debug bugs, and race conditions. State management patterns impose structure to make state changes predictable.

Key approaches:
- **Flux/Redux** — Unidirectional data flow, single store, pure reducers
- **MobX** — Observable state, automatic dependency tracking
- **XState** — Explicit state machines (finite automata)
- **Jotai/Recoil** — Atomic state (bottom-up composition)
- **Zustand** — Simplified Redux-like store

## 🔍 Code Examples

### Redux Pattern (from Scratch)

```javascript
function createStore(reducer, initialState, enhancer) {
  if (enhancer) return enhancer(createStore)(reducer, initialState)
  
  let state = initialState
  const listeners = new Set()
  let dispatching = false
  
  function getState() {
    if (dispatching) throw new Error('Cannot read state during dispatch')
    return state
  }
  
  function subscribe(listener) {
    if (dispatching) throw new Error('Cannot subscribe during dispatch')
    listeners.add(listener)
    return () => {
      if (dispatching) throw new Error('Cannot unsubscribe during dispatch')
      listeners.delete(listener)
    }
  }
  
  function dispatch(action) {
    if (dispatching) throw new Error('Reducers must not dispatch actions')
    dispatching = true
    try {
      state = reducer(state, action)
    } finally {
      dispatching = false
    }
    listeners.forEach(l => l())
    return action
  }
  
  dispatch({ type: '@@INIT' })
  
  return { getState, subscribe, dispatch }
}
```

### XState-Inspired State Machine

```javascript
class StateMachine {
  constructor({ initial, states }) {
    this.current = initial
    this.states = states
    this.listeners = new Set()
  }
  
  send(event) {
    const stateConfig = this.states[this.current]
    if (!stateConfig) throw new Error(`Unknown state: ${this.current}`)
    
    const transition = stateConfig.on?.[event]
    if (!transition) {
      console.warn(`No transition for event "${event}" in state "${this.current}"`)
      return
    }
    
    const target = typeof transition === 'string' ? transition : transition.target
    
    // Exit action
    stateConfig.exit?.()
    
    // Transition action
    if (typeof transition === 'object') transition.action?.()
    
    this.current = target
    
    // Entry action
    this.states[target]?.entry?.()
    
    this.listeners.forEach(l => l(this.current))
  }
  
  onTransition(fn) {
    this.listeners.add(fn)
    return () => this.listeners.delete(fn)
  }
}

const orderMachine = new StateMachine({
  initial: 'idle',
  states: {
    idle: { on: { SUBMIT: 'validating' } },
    validating: {
      entry: () => runValidation(),
      on: {
        VALID: 'processing',
        INVALID: { target: 'error', action: () => showValidationErrors() }
      }
    },
    processing: {
      entry: () => submitOrder(),
      on: { SUCCESS: 'success', FAILURE: 'error' }
    },
    success: { on: { RESET: 'idle' } },
    error: { on: { RETRY: 'validating', RESET: 'idle' } }
  }
})
```

## 🏢 Industry Best Practices

1. **Keep state normalized** — No nested/duplicated state. Single source of truth.
2. **Immutable updates** — Always return new state objects from reducers.
3. **Colocate state with usage** — Not everything belongs in global store.
4. **Use selectors/memoization** — Prevent recomputation on unrelated state changes.
5. **State machines for complex UI** — Form flows, async operations, multi-step wizards.

## 💼 Interview Questions

**Q1: Why does Redux require pure reducers?**
> Pure reducers (no side effects, same input → same output) enable: (1) time-travel debugging — replay actions on the pure function to reconstruct any previous state; (2) server-side rendering — initial state is serialized and sent to client; (3) testing — trivially test with input/output without mocks; (4) hot reloading — swap reducer code without losing state. Side effects in reducers would break all of these.

## 🔗 Navigation

**Prev:** [07_Reactive_Patterns.md](07_Reactive_Patterns.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [../Performance/01_Code_Optimization.md](../Performance/01_Code_Optimization.md)
