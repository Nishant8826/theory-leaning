# 📌 Project 01 — Build Event Emitter From Scratch

## 🎯 Goal

Build a production-grade EventEmitter with the following features:
- `.on()`, `.off()`, `.once()`, `.emit()`
- Wildcard events (`*`)
- Async event support
- Priority-ordered handlers
- Automatic cleanup via AbortSignal
- Memory leak warnings

## 📋 Requirements

```
1. Basic: on/off/emit/once
2. Priority: handlers execute in priority order
3. Wildcard: bus.on('*', handler) catches all events
4. Async: emitAsync waits for all async handlers
5. AbortSignal: auto-cleanup when signal aborts
6. MaxListeners: warn when threshold exceeded
7. Error isolation: one throwing handler doesn't stop others
```

## ✅ Complete Solution

See Interview/03_Coding_Problems.md — Problem 5 for complete EventEmitter implementation.

## 🧪 Test Cases

```javascript
const emitter = new EventEmitter()

// Test 1: Basic on/emit
let count = 0
emitter.on('test', () => count++)
emitter.emit('test')
emitter.emit('test')
assert(count === 2, 'Basic on/emit failed')

// Test 2: Once
let onceCount = 0
emitter.once('once-test', () => onceCount++)
emitter.emit('once-test')
emitter.emit('once-test')
assert(onceCount === 1, 'once() should only fire once')

// Test 3: Off
let offCount = 0
const handler = () => offCount++
emitter.on('off-test', handler)
emitter.emit('off-test')
emitter.off('off-test', handler)
emitter.emit('off-test')
assert(offCount === 1, 'off() should remove listener')

// Test 4: Error isolation
let ran = false
emitter.on('error-test', () => { throw new Error('test') })
emitter.on('error-test', () => { ran = true })
emitter.emit('error-test')
assert(ran === true, 'Error in one handler should not stop others')

// Test 5: Listener count
emitter.on('count-test', () => {})
emitter.on('count-test', () => {})
assert(emitter.listenerCount('count-test') === 2)
```

## 🔗 Navigation

**Index:** [../00_Index.md](../00_Index.md) | **Next:** [02_Build_Promise.md](02_Build_Promise.md)
