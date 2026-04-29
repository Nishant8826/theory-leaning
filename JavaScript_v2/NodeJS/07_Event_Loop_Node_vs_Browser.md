# 📌 07 — Event Loop: Node.js vs Browser

## 🧠 Concept Explanation

While both Node.js and browsers use a single-threaded event loop model, they have significant differences in implementation and phase structure.

## 🔬 Comparison

| Aspect | Browser | Node.js |
|--------|---------|---------|
| Implementation | Each browser's engine | libuv |
| Phases | Task queue + microtask | 6 phases (timer/pending/poll/check/close) |
| Timer precision | ~1ms (4ms clamped) | ~1ms (OS resolution) |
| setImmediate | Not available | Check phase (after poll) |
| process.nextTick | Not available | Before each phase (nextTick queue) |
| rAF | Available (display sync) | Not available |
| I/O source | Network (XHR, fetch) | Network + file system + child process |

## 🔍 Code Examples

### Key Behavioral Differences

```javascript
// Node.js specific: process.nextTick vs setImmediate
setImmediate(() => console.log('setImmediate'))
process.nextTick(() => console.log('nextTick'))
Promise.resolve().then(() => console.log('Promise'))
console.log('sync')

// Output: sync, nextTick, Promise, setImmediate
// nextTick runs before promises (separate queue, checked between each phase)

// Browser equivalent (no nextTick, no setImmediate):
setTimeout(() => console.log('setTimeout'), 0)
Promise.resolve().then(() => console.log('Promise'))
console.log('sync')
// Output: sync, Promise, setTimeout
```

### Node.js setImmediate vs setTimeout(0)

```javascript
// INSIDE I/O callback: setImmediate ALWAYS before setTimeout
fs.readFile('file', () => {
  setTimeout(() => console.log('timeout'))  // timers phase (next iteration)
  setImmediate(() => console.log('immediate'))  // check phase (THIS iteration)
  // Output always: immediate, timeout
})

// OUTSIDE I/O callback: ORDER IS UNDEFINED (depends on timing)
setTimeout(() => console.log('timeout'))  // May be before or after immediate
setImmediate(() => console.log('immediate'))  // May be before or after timeout
// Depends on whether the loop has time to reach timers phase before check
```

## 💥 Production Failure — nextTick Starvation

```javascript
// process.nextTick callbacks can starve the event loop
function endlessNextTick() {
  process.nextTick(endlessNextTick)  // Recursively adds nextTick
}
endlessNextTick()

// Result: event loop NEVER advances to I/O phases
// All network, file, timer callbacks queued forever
// Process appears to hang despite running

// Node.js does NOT limit nextTick queue depth (unlike browser)
// Even setImmediate cannot starve (it's a phase, not a queue)
// Fix: Use setImmediate for recursive scheduling
```

## 🏢 Industry Best Practices

1. **Prefer setImmediate over process.nextTick for recursive scheduling** — Avoids starvation.
2. **Use process.nextTick for error propagation** — Ensures errors propagate before I/O.
3. **Don't use setTimeout(fn, 0) in Node.js for immediate execution** — Use setImmediate or nextTick.
4. **Test phase-specific behavior** — Different event loop phases can change execution order.

## 💼 Interview Questions

**Q1: Why does setImmediate always run before setTimeout(0) inside I/O callbacks?**
> When inside an I/O callback (poll phase), you're already past the timers phase for this event loop iteration. setImmediate callbacks run in the check phase, which comes AFTER the poll phase in the same iteration. setTimeout(0) callbacks run in the timers phase of the NEXT iteration. So inside an I/O callback, setImmediate always wins. Outside I/O callbacks, the race depends on OS timer resolution.

## 🔗 Navigation

**Prev:** [06_Middleware_Design.md](06_Middleware_Design.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [08_Backpressure_Deep_Dive.md](08_Backpressure_Deep_Dive.md)
