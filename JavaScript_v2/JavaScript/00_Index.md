# 📚 Advanced JavaScript Deep Dive — Master Index

> **Target Audience:** Senior / Staff / Principal Engineers with 10+ years experience  
> **Focus:** Engine internals, production debugging, performance, runtime behavior  
> **Engine Coverage:** V8 (Ignition + TurboFan), libuv, Blink/WebKit/Gecko, Node.js

---

## 🗺️ Course Philosophy

This course does **not** teach JavaScript syntax. It teaches **how JavaScript actually works** — at the V8 bytecode level, at the libuv thread pool level, at the browser compositor thread level, and at the point where JS objects cross the C++ boundary into the DOM.

Every file follows the rule: **If it doesn't explain WHY the behavior exists at the engine level, it is invalid.**

---

## 🧭 Learning Path (Recommended Order)

```
Runtime Fundamentals → Memory & GC → Async Model → Browser Engine
       ↓                                                   ↓
  Node.js Internals ←————— Concurrency ————————→ Performance
       ↓                                                   ↓
  Design Patterns ←—————— Systems Thinking ————→ Interview Prep
       ↓
  Production Projects
```

---

## 📂 Module Breakdown

### 📂 Fundamentals — Engine Runtime Core

| # | File | Key Internals Covered |
|---|------|-----------------------|
| 01 | [Execution Context](Fundamentals/01_Execution_Context.md) | EC lifecycle, LexicalEnvironment, VariableEnvironment, Realm |
| 02 | [Call Stack](Fundamentals/02_Call_Stack.md) | Stack frames, V8 stack limit, stack overflow internals |
| 03 | [Hoisting](Fundamentals/03_Hoisting.md) | TDZ mechanics, binding creation phase, V8 AST pass |
| 04 | [Scope & Lexical Environment](Fundamentals/04_Scope_and_Lexical_Environment.md) | Scope chain, environment records, IIFE optimization |
| 05 | [Closures](Fundamentals/05_Closures.md) | Heap-allocated frames, context retention, GC implications |
| 06 | [This Keyword](Fundamentals/06_This_Keyword.md) | Implicit binding, explicit binding, arrow lexical this |
| 07 | [Prototype & Inheritance](Fundamentals/07_Prototype_and_Inheritance.md) | [[Prototype]] chain, hidden classes, property lookup cost |
| 08 | [Event Loop](Fundamentals/08_Event_Loop.md) | Phases, microtask checkpoint, rendering coordination |
| 09 | [Promises](Fundamentals/09_Promises.md) | PromiseReactionJob, microtask enqueue, unhandled rejection |
| 10 | [Async/Await](Fundamentals/10_Async_Await.md) | Generator suspension, implicit promise, resume mechanics |
| 11 | [Microtasks vs Macrotasks](Fundamentals/11_Microtasks_vs_Macrotasks.md) | Queue priorities, starvation, browser vs Node |
| 12 | [Execution Order Deep Dive](Fundamentals/12_Execution_Order_Deep_Dive.md) | Full trace: sync → micro → render → macro |

---

### 📂 Advanced — V8 Internals & Memory

| # | File | Key Internals Covered |
|---|------|-----------------------|
| 01 | [Deep vs Shallow Copy](Advanced/01_Deep_vs_Shallow_Copy.md) | Structural sharing, COW, serialization cost |
| 02 | [Memory Management](Advanced/02_Memory_Management.md) | Heap layout, new/old space, pointer compression |
| 03 | [Garbage Collection](Advanced/03_Garbage_Collection.md) | Orinoco, incremental marking, write barriers |
| 04 | [Concurrency Model](Advanced/04_Concurrency_Model.md) | SAB, Atomics, lock-free data structures |
| 05 | [Debouncing vs Throttling](Advanced/05_Debouncing_vs_Throttling.md) | Timer drift, RAF alternative, production patterns |
| 06 | [Currying](Advanced/06_Currying.md) | Partial application, arity, IC implications |
| 07 | [Composition vs Inheritance](Advanced/07_Composition_vs_Inheritance.md) | Mixin cost, hidden class pollution |
| 08 | [Immutability](Advanced/08_Immutability.md) | Structural sharing, persistent data structures |
| 09 | [Modules System](Advanced/09_Modules_System.md) | ESM vs CJS loader, live bindings, circular deps |
| 10 | [Proxy & Reflect](Advanced/10_Proxy_and_Reflect.md) | Trap cost, IC invalidation, Reflect internals |
| 11 | [Symbols & Iterators](Advanced/11_Symbols_and_Iterators.md) | Well-known symbols, protocol internals |
| 12 | [TypedArrays & ArrayBuffers](Advanced/12_TypedArrays_and_ArrayBuffers.md) | Memory layout, SIMD, SharedArrayBuffer |

---

### 📂 Browser — Rendering Engine & APIs

| # | File | Key Internals Covered |
|---|------|-----------------------|
| 01 | [DOM Manipulation](Browser/01_DOM_Manipulation.md) | C++↔JS bridge, DOM binding cost, layout invalidation |
| 02 | [Event Delegation](Browser/02_Event_Delegation.md) | Bubble/capture phase, listener memory cost |
| 03 | [Browser Storage](Browser/03_Browser_Storage.md) | IndexedDB internals, storage quotas, eviction |
| 04 | [Service Workers](Browser/04_Service_Workers.md) | Lifecycle, fetch interception, cache strategy |
| 05 | [Rendering Pipeline](Browser/05_Rendering_Pipeline.md) | Critical path, layer promotion, compositor thread |
| 06 | [CORS](Browser/06_CORS.md) | Preflight, CORB, COEP/COOP headers |
| 07 | [Web Workers](Browser/07_Web_Workers.md) | Dedicated vs shared workers, postMessage cost |
| 08 | [Intersection Observer](Browser/08_Intersection_Observer_and_Performance.md) | IntersectionObserver internals, threshold math |
| 09 | [Animation & Frame Budget](Browser/09_Animation_and_Frame_Budget.md) | 16ms budget, RAF scheduling, jank analysis |

---

### 📂 NodeJS — Runtime Architecture

| # | File | Key Internals Covered |
|---|------|-----------------------|
| 01 | [Node Architecture](NodeJS/01_Node_Architecture.md) | V8 + libuv integration, binding layer, bootstrap |
| 02 | [Event Emitter](NodeJS/02_Event_Emitter.md) | Listener management, memory leaks, async emitters |
| 03 | [Streams](NodeJS/03_Streams.md) | Readable internals, highWaterMark, objectMode |
| 04 | [Cluster Module](NodeJS/04_Cluster_Module.md) | IPC, load balancing, shared ports |
| 05 | [Worker Threads](NodeJS/05_Worker_Threads.md) | MessageChannel, SharedArrayBuffer, thread sync |
| 06 | [Middleware Design](NodeJS/06_Middleware_Design.md) | Koa vs Express compose, error propagation |
| 07 | [Event Loop Node vs Browser](NodeJS/07_Event_Loop_Node_vs_Browser.md) | libuv phases, setImmediate vs setTimeout |
| 08 | [Backpressure Deep Dive](NodeJS/08_Backpressure_Deep_Dive.md) | Stream pause/resume, pipe, drain event |

---

### 📂 Patterns — Design & Architecture

| # | File | Key Internals Covered |
|---|------|-----------------------|
| 01 | [Module Pattern](Patterns/01_Module_Pattern.md) | IIFE, revealing module, ESM comparison |
| 02 | [Factory Pattern](Patterns/02_Factory_Pattern.md) | Object creation cost, hidden class impact |
| 03 | [Singleton Pattern](Patterns/03_Singleton_Pattern.md) | Module-level singletons, testing problems |
| 04 | [Observer Pattern](Patterns/04_Observer_Pattern.md) | Push vs pull, memory leak risk |
| 05 | [Strategy Pattern](Patterns/05_Strategy_Pattern.md) | Polymorphic dispatch, IC implications |
| 06 | [Middleware Pattern](Patterns/06_Middleware_Pattern.md) | Compose internals, error boundaries |
| 07 | [Reactive Patterns](Patterns/07_Reactive_Patterns.md) | Observable internals, schedulers, backpressure |
| 08 | [State Management Patterns](Patterns/08_State_Management_Patterns.md) | Flux, Redux internals, signal-based state |

---

### 📂 Performance — Optimization & Profiling

| # | File | Key Internals Covered |
|---|------|-----------------------|
| 01 | [Code Optimization](Performance/01_Code_Optimization.md) | Monomorphic functions, loop unrolling, inlining |
| 02 | [Reflow & Repaint](Performance/02_Reflow_and_Repaint.md) | Layout invalidation, forced sync layout |
| 03 | [Memory Leaks](Performance/03_Memory_Leaks.md) | Retained size, detached nodes, closure leaks |
| 04 | [Lazy Loading](Performance/04_Lazy_Loading.md) | Dynamic import, module graph, bundle splitting |
| 05 | [Bundle Optimization](Performance/05_Bundle_Optimization.md) | Tree shaking, scope hoisting, code splitting |
| 06 | [Deoptimization & ICs](Performance/06_Deoptimization_and_ICs.md) | IC states, deopt triggers, --trace-deopt |
| 07 | [Event Loop Blocking UI](Performance/07_Event_Loop_Blocking_UI.md) | Long tasks, scheduler API, isInputPending |
| 08 | [GC Performance Tuning](Performance/08_GC_Performance_Tuning.md) | GC pauses, allocation rate, --expose-gc |

---

### 📂 Interview — Senior/Staff/Principal Prep

| # | File | Key Internals Covered |
|---|------|-----------------------|
| 01 | [JS Interview Core](Interview/01_JS_Interview_Core.md) | 30+ deep questions with engine-level answers |
| 02 | [Tricky Questions](Interview/02_Tricky_Questions.md) | Output prediction, async traps, coercion |
| 03 | [Coding Problems](Interview/03_Coding_Problems.md) | DSA in JS with V8 performance awareness |
| 04 | [Machine Coding](Interview/04_Machine_Coding_JS.md) | System design at code level, production patterns |

---

### 📂 Projects — Production-Grade Implementations

| # | File | Key Internals Covered |
|---|------|-----------------------|
| 01 | [Build Event Emitter](Projects/01_Build_Event_Emitter.md) | Memory management, once/off, wildcard |
| 02 | [Build Promise](Projects/02_Build_Promise.md) | State machine, microtask scheduling, chaining |
| 03 | [Build LRU Cache](Projects/03_Build_LRU_Cache.md) | Doubly linked list + Map, O(1) ops |
| 04 | [Build React-Like State](Projects/04_Build_React_Like_State.md) | Fiber-like scheduling, batching, hooks |
| 05 | [Build Rate Limiter](Projects/05_Build_Rate_Limiter.md) | Token bucket, sliding window, Redis pattern |
| 06 | [Real-Time Chat](Projects/06_Real_Time_Chat.md) | WebSocket, backpressure, reconnection |

---

## 🔗 Quick Reference Links

- **Start here (runtime model):** [Execution Context →](Fundamentals/01_Execution_Context.md)
- **V8 optimization guide:** [Deoptimization & ICs →](Performance/06_Deoptimization_and_ICs.md)
- **Async deep dive:** [Event Loop →](Fundamentals/08_Event_Loop.md)
- **Production debugging:** [Memory Leaks →](Performance/03_Memory_Leaks.md)
- **Interview prep:** [JS Interview Core →](Interview/01_JS_Interview_Core.md)

---

## 🧑‍💻 How to Use This Course

1. **Don't skip Fundamentals** — even if you know closures, the engine-level sections will reveal non-obvious behavior
2. **Run the code examples** with `node --trace-opt --trace-deopt` to see V8's decisions
3. **Use Chrome DevTools** → Performance tab for every Browser topic
4. **For Node topics**, use `node --inspect` + clinic.js flame graphs
5. **Interview files** are structured for active recall — attempt answers before reading solutions

---

*Generated for Senior/Staff/Principal JavaScript engineers. All content assumes deep ES6+ knowledge.*
