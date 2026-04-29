# 📌 07 — Native Addons (Node-API): The C++ Powerhouse

## 🧠 Concept Explanation

### Basic → Intermediate
Native Addons are dynamically linked shared objects written in C or C++ that can be loaded into Node.js using `require()`. They allow you to perform tasks that are difficult or slow in JavaScript, such as high-performance image processing or direct hardware access.

### Advanced → Expert
The modern way to build addons is via **Node-API (formerly N-API)**.
Node-API provides an ABI (Application Binary Interface) stability guarantee. This means that an addon compiled for Node 12 will work on Node 14, 16, or 18 without recompilation. 

Internally, Node-API is a C header file that wraps the complex V8 and libuv APIs. This isolates the addon developer from the rapid changes in the V8 internal engine.

---

## 🏗️ Common Mental Model
"C++ is always faster than JavaScript."
**Correction**: C++ logic is faster, but **crossing the boundary** from JS to C++ is expensive. If you call a C++ function 1 million times for a tiny task (like adding two numbers), the overhead of the V8 API call will make it slower than pure JavaScript.

---

## ⚡ Actual Behavior: Memory Mapping
Native addons can use `v8::ArrayBuffer` to map C++ memory directly into JavaScript without copying. This "Zero-copy" approach is essential for high-performance networking or video processing.

---

## 🔬 Internal Mechanics (V8 + Node.js Bindings)

### The JS ↔ C++ Boundary Cost
1. **Argument Validation**: V8 must check that the inputs match the C++ signature.
2. **Type Conversion**: JS `Number` (Double) to C++ `int`.
3. **HandleScope**: Creating references to JS objects so the GC doesn't collect them while C++ is using them.
4. **Bailout**: If the call fails, V8 must handle the exception and return to the JS event loop.

---

## 📐 ASCII Diagrams

### Node-API Bridge
```text
  ┌────────────────────────┐         ┌────────────────────────┐
  │   JAVASCRIPT (V8)      │         │   NATIVE C++ ADDON     │
  │                        │         │                        │
  │  const addon =         │         │  napi_value Method(    │
  │    require('./my.node')│         │    napi_env env,       │
  │                        │         │    napi_callback_info  │
  │  addon.expensiveTask() ├────────▶│  ) { ... }             │
  └────────────────────────┘         └────────────────────────┘
               │                                  │
               └───────────[ NODE-API ]───────────┘
               (ABI Stable Boundary / No Re-compile)
```

---

## 🔍 Code Example: Simple Node-API C++
```cpp
// hello.cpp
#include <node_api.h>

napi_value Method(napi_env env, napi_callback_info info) {
  napi_value world;
  napi_create_string_utf8(env, "world", 5, &world);
  return world;
}

napi_value Init(napi_env env, napi_value exports) {
  napi_value fn;
  napi_create_function(env, NULL, 0, Method, NULL, &fn);
  napi_set_named_property(env, exports, "hello", fn);
  return exports;
}

NAPI_MODULE(NODE_GYP_MODULE_NAME, Init)
```

---

## 💥 Production Failures & Debugging

### Scenario: The Hidden Memory Leak (Native)
**Problem**: The process RSS is 4GB, but JS Heap is 50MB. Heap snapshots show nothing.
**Reason**: You are using a native addon (like a database driver or an image library) that allocates memory in C++ using `new` or `malloc` but fails to `delete` or `free` it in the destructor or cleanup callback.
**Debug**: Use **Valgrind** or **AddressSanitizer (ASan)** to track native memory allocations.
**Fix**: Fix the C++ leak and ensure `napi_add_finalizer` is used to clean up native data when the JS wrapper object is GC'd.

---

## 🧪 Real-time Production Q&A

**Q: "Should I rewrite my crypto logic in C++ for performance?"**
**A**: **Probably Not.** Node's built-in `crypto` module is already a wrapper around highly optimized OpenSSL C code. Unless you have a custom algorithm not in OpenSSL, you won't beat the built-in performance.

---

## 🧪 Debugging Toolchain
- **`node-gyp`**: The standard tool for compiling C++ addons into `.node` files.
- **`nm -C my.node`**: View the symbols in your compiled addon to verify exports.

---

## 🏢 Industry Best Practices
- **Prefer Node-API**: Avoid direct V8/NAN (Native Abstractions for Node) APIs unless you need extremely low-level access that Node-API doesn't provide.
- **Offload to Thread Pool**: If your native function takes > 5ms, use `napi_create_async_work` to run it in the libuv thread pool so you don't block the JS event loop.

---

## 💼 Interview Questions
**Q: What is ABI Stability and why does it matter?**
**A**: Application Binary Interface (ABI) stability ensures that the binary interface between Node.js and the addon remains constant. It matters because it allows addon authors to ship pre-compiled binaries that work across multiple Node.js versions, saving users from having to install C++ build tools.

---

## 🧩 Practice Problems
1. Compile a "Hello World" addon using `node-gyp`.
2. Measure the latency of calling a C++ function that does nothing vs a JS function that does nothing. Calculate the "Boundary Crossing Cost" on your machine.

---

**Prev:** [06_Process_Model.md](./06_Process_Model.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [08_Diagnostics_Channel.md](./08_Diagnostics_Channel.md)
