# V8 Engine

JavaScript is dynamically typed, which means the runtime does not know variable types until execution. In a static language (like C++), compiler offsets are resolved during compile time. V8 does this on the fly. Knowing how V8 compiles code allows you to write JavaScript that aligns with the engine's optimization pipeline, yielding production-grade code that executes at near-native speeds.

### The V8 Compiler Pipeline
JavaScript code cannot be run directly by physical CPU cores; it must be compiled into machine code. V8 achieves this using JIT (Just-In-Time) compilation:

1. **Parser**: Parses source code into an **Abstract Syntax Tree (AST)**.
2. **Ignition Interpreter**: Compiles the AST into bytecode. As the bytecode executes, Ignition monitors execution statistics (hot spot profiling) to see which functions run frequently.
3. **TurboFan Optimizing Compiler**: Extracts "hot" functions from Ignition along with feedback data (type profiles) and compiles them into highly optimized machine code.
4. **Deoptimization (Deopt)**: If the type profiles of a hot function change during runtime (e.g. passing a string instead of an expected integer), TurboFan throws away the optimized machine code and falls back to Ignition's bytecode execution.

### Hidden Classes (Shapes) and Inline Caches
In JavaScript, objects can have properties dynamically added or removed. To optimize property lookups without searching hash tables every time, V8 creates internal **Hidden Classes** (also called **Shapes**).

When you access an object property (e.g., `obj.x`), V8 maps the object to its hidden class. If it accesses the property multiple times at the same location, it uses an **Inline Cache (IC)**. The IC remembers the memory offset of the property directly within the object representation, skipping the hidden class lookup entirely.

## Deep Dive

### The Structure of the V8 Heap
The V8 Heap houses dynamic memory allocations. It is split into different spaces to optimize Garbage Collection:
1. **New Space (Young Generation)**: A small, high-speed buffer where all new objects are initially allocated. It uses a scavenger collection algorithm.
2. **Old Space (Old Generation)**: Objects that survive multiple garbage collection passes in the New Space are promoted to the Old Space. It is divided into:
   * **Old Pointer Space**: Contains objects that reference other objects.
   * **Old Data Space**: Contains raw data payloads (strings, raw arrays, buffers).
3. **Large Object Space**: For objects too large to fit into the New Space. These are never garbage collected by the scavenger; they require major collection cycles.
4. **Code Space**: Where TurboFan compiled machine code payloads are written. This space has execution permissions.

### Optimization and Deoptimization Pathways
To keep TurboFan code fast:
* **Monomorphic call sites**: An operation receives objects of the exact same Shape. (V8 can cache offset addresses easily).
* **Polymorphic call sites**: An operation receives 2-4 different Shapes. (Slightly slower; V8 must check a list of cached offsets).
* **Megamorphic call sites**: An operation receives 5+ different Shapes. (Slow; V8 defaults to a generic dictionary lookup).

## Visual Explanation

### V8 Engine Compilation Pipeline
```text
  [ JS Source Code ]
          │
          ▼
     [ Parser ] ───> [ Abstract Syntax Tree (AST) ]
                              │
                              ▼
                    [ Ignition Interpreter ] <───────┐ (Deopt: Fallback)
                              │                      │
                              ├─── [Bytecode]        │
                              ▼                      │
                     [ Profiler / Monitor ]          │
                              │                      │
                   (If function is "Hot")            │
                              │                      │
                              ▼                      │
                    [ TurboFan Compiler ] ───────────┘
                              │
                              ▼
                     [ Machine Code ]
```

## Real-World Example
Suppose you create a function that parses database records:
```javascript
function processRecord(record) {
  return record.id + record.value;
}
```
If you pass records of shape `{ id: 1, value: 100 }`, V8 compiles optimized machine code. If you later pass a record containing a different shape, such as `{ value: 100, id: 2, timestamp: 99120 }`, V8 must **deoptimize** the function, discard the machine code, and rebuild shapes. This slows down processing.

## Code Examples

### Hidden Classes and Deoptimization Demonstration

```javascript
// Helper to verify V8 optimization status (Run with: node --allow-natives-syntax script.js)
// Note: %GetOptimizationStatus and %OptimizeFunctionOnNextCall are V8 intrinsic helpers.

class Point {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }
}

// 1. Instantiating objects with identical shapes (Monomorphic)
const p1 = new Point(1, 2);
const p2 = new Point(3, 4);

function addCoordinates(point) {
  return point.x + point.y;
}

// Warm up the function to make V8 flag it as "hot"
addCoordinates(p1);
addCoordinates(p2);

// Force optimization
if (typeof %OptimizeFunctionOnNextCall === 'function') {
  %OptimizeFunctionOnNextCall(addCoordinates);
}
addCoordinates(p1); // Invoked optimized code

// 2. Breaking the shape hierarchy dynamically
const p3 = new Point(5, 6);
p3.z = 7; // Adds a new property, creating a new hidden class (Shape change)

// This call forces a deoptimization because the input shape changed!
addCoordinates(p3); 

if (typeof %GetOptimizationStatus === 'function') {
  const status = %GetOptimizationStatus(addCoordinates);
  console.log('Optimization Status Code:', status);
  // Status codes: 1 = Optimized, 2 = Not Optimized (Deoptimized)
}
```

## Best Practices
* **Initialize Properties in the Constructor**: Always declare all class fields inside the constructor in the exact same order. Never inject properties dynamically (`obj.newField = 1`) after initialization.
* **Avoid Deletes**: Do not use the `delete` keyword on objects. It alters the object's shape, converting it into a slow dictionary-lookup hash map. Instead, set unused properties to `null` or `undefined`.
* **Use Constant Variable Types**: Avoid changing variable types inside functions (e.g. keeping variable `a` as a number, instead of assigning a string to it later).

## Interview Questions

**Q:** What is the V8 engine and where is it used?

> **Answer:**
> V8 is Google’s open-source High-Performance JavaScript and WebAssembly engine. It is written in C++ and is used inside Google Chrome and the Node.js runtime environment to compile JavaScript directly into native machine code.

**Q:** Explain how JIT compilation works in Node.js.

> **Answer:**
> V8 does not compile all code to machine code up front. It initially parses the code and generates bytecode using the Ignition Interpreter. While executing, it monitors the execution metrics to spot "hot" functions. It then passes these hot functions to the TurboFan compiler, which compiles them into optimized machine code based on runtime type data.

**Q:** What are Hidden Classes (Shapes) and how do dynamic changes to objects affect V8’s execution performance?

> **Answer:**
> Since JavaScript is dynamic, V8 creates internal "Hidden Classes" (Shapes) that define the offsets of object properties in memory. When properties are dynamically added, deleted, or initialized in different orders, V8 must generate new hidden classes and transition maps. This invalidates Inline Caches (ICs) and forces the TurboFan compiler to deoptimize hot code, reverting to slower interpreter bytecodes or dictionary lookups.

**Q:** Describe the structural layout of V8 heap generations. How does the scavenger algorithm operate differently from the major mark-sweep-compact collector, and how does this affect application performance spikes?

> **Answer:**
> The V8 heap is divided into the Young Generation (New Space, composed of two semi-spaces: To-space and From-space) and the Old Generation (Old Space).

**Q:** Scavenger Collection

> **Answer:**
> 

**Q:** Major Garbage Collection

> **Answer:**
> 

---
Previous : [04_Runtime_vs_Framework.md](04_Runtime_vs_Framework.md) | Index : [00_index.md](00_index.md) | Next : [06_Event_Loop_Basics.md](06_Event_Loop_Basics.md)
