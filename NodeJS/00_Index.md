# 🚀 Node.js Systems Engineering & Runtime Internals

## 🛰️ Course Roadmap: From Intermediate to Staff Engineer

This curriculum is designed for senior engineers with 10+ years of experience who want to master the **Node.js Runtime**, **V8 Engine**, and **Low-Level Systems Engineering**. We bypass beginner analogies and "hello world" examples, focusing instead on memory layouts, kernel syscalls, event loop phases, and production-grade debugging.

---

## 🗺️ Learning Path

### 🏗️ Section 1: Core Architecture
Understanding the bridge between JavaScript and C++.
- [01_Node_Architecture.md](./Core/01_Node_Architecture.md) - The V8 / libuv / Node.js relationship.
- [02_Event_Loop_Deep_Dive.md](./Core/02_Event_Loop_Deep_Dive.md) - Beyond the "circle" diagram.
- [03_Non_Blocking_IO.md](./Core/03_Non_Blocking_IO.md) - Epoll, Kqueue, and IOCP internals.
- [04_Callbacks_Promises_Async.md](./Core/04_Callbacks_Promises_Async.md) - Microtask queue mechanics.
- [05_Error_Handling.md](./Core/05_Error_Handling.md) - Boundary crossing and crash safety.
- [07_Event_Emitter_Deep_Dive.md](./Core/07_Event_Emitter_Deep_Dive.md) - Observer pattern at scale.
- [08_Timers_Internals.md](./Core/08_Timers_Internals.md) - Timer drift and binary heaps.
- [09_Async_Hooks_and_Context.md](./Core/09_Async_Hooks_and_Context.md) - Managing async state.

### ⚙️ Section 2: Runtime & V8
The engine room of execution.
- [01_V8_Integration.md](./Runtime/01_V8_Integration.md) - Ignition, TurboFan, and JIT.
- [02_Memory_Management.md](./Runtime/02_Memory_Management.md) - Heap, Stack, and Off-heap memory.
- [03_Garbage_Collection.md](./Runtime/03_Garbage_Collection.md) - Scavenge vs Mark-Compact vs Parallel GC.
- [04_Worker_Threads.md](./Runtime/04_Worker_Threads.md) - SharedArrayBuffer and multi-core Node.
- [05_Cluster_Module.md](./Runtime/05_Cluster_Module.md) - Round-robin vs OS-level load balancing.

### 🌐 Section 3: Networking & Protocols
Building high-throughput communication stacks.
- [01_HTTP_Server_Internals.md](./Networking/01_HTTP_Server_Internals.md) - Node's http_parser and llhttp.
- [06_TLS_SSL_Deep_Dive.md](./Networking/06_TLS_SSL_Deep_Dive.md) - OpenSSL integration and handshake overhead.
- [07_HTTP2_and_HTTP3.md](./Networking/07_HTTP2_and_HTTP3.md) - Multiplexing and QUIC.

### 📉 Section 4: Performance & Observability
Debugging what you can't see.
- [01_Event_Loop_Blocking.md](./Performance/01_Event_Loop_Blocking.md) - Detection and remediation.
- [02_Profiling_and_Debugging.md](./Performance/02_Profiling_and_Debugging.md) - Flamegraphs, Heap Snapshots, and perf.
- [04_Streams_and_Buffers.md](./Performance/04_Streams_and_Buffers.md) - Zero-copy buffer management.

---

## 🎯 Suggested Progression
1. **Internals First**: Start with `Internals/` to build a mental model of libuv and syscalls.
2. **Runtime Mastery**: Move to `Runtime/` to understand how V8 consumes your code.
3. **Systems Design**: Apply that knowledge to `Architecture/` and `Scaling/`.
4. **Hands-on Implementation**: Complete the `Projects/` to build complex systems from scratch.

---

## 🛠️ Prerequisites
- Deep familiarity with ES2022+ syntax.
- Basic understanding of C++ (for native addon context).
- Familiarity with Linux/Unix terminal and system signals.

**Next:** [01_Node_Architecture.md](./Core/01_Node_Architecture.md)
