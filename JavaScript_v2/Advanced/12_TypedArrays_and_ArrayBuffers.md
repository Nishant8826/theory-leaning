# 📌 12 — TypedArrays & ArrayBuffers

## 🧠 Concept Explanation

TypedArrays and ArrayBuffers provide access to raw binary memory from JavaScript — essential for WebGL, WebAssembly, audio processing, network protocols, and file I/O. They bypass the V8 object heap and work directly with memory allocated by the ArrayBuffer allocator.

Key hierarchy:
```
ArrayBuffer — raw fixed-length binary buffer (bytes)
  ↓ viewed through
TypedArray (Int8Array, Uint8Array, Float32Array, BigInt64Array, etc.)
  OR
DataView — heterogeneous reads/writes at arbitrary byte offsets
```

SharedArrayBuffer extends this to allow sharing across Workers without copying.

## 🔬 Internal Mechanics (V8)

### Memory Layout

```
ArrayBuffer (C++ backing store):
┌──────────────────────────────────────────────────────────────┐
│  Raw bytes (not V8 object heap — separate allocator)         │
│  [byte0][byte1][byte2]...[byteN]                            │
└──────────────────────────────────────────────────────────────┘
         ↑
JSArrayBuffer (V8 heap object):
         ┌─────────────────────────────────────────┐
         │  backing_store_ref → [pointer to bytes] │
         │  byte_length: N                         │
         └─────────────────────────────────────────┘
         ↑
JSTypedArray (V8 heap object, extends JSArrayBufferView):
         ┌─────────────────────────────────────────┐
         │  buffer → JSArrayBuffer                 │
         │  byte_offset: 0                         │
         │  byte_length: N                         │
         │  length: N / element_size               │
         └─────────────────────────────────────────┘
```

The backing store allocation is tracked as "external memory" by V8 — it adjusts GC scheduling based on external memory size to prevent OOM.

### V8 TypedArray Element Access

TypedArray element access is a highly optimized path in V8:
- `typedArray[i]` → bounds check (JSTypedArray.length) → raw memory read
- No property lookup, no hidden class check (TypedArrays have fixed element kinds)
- TurboFan generates near-native-speed machine code for TypedArray loops

```javascript
// This is heavily optimized by V8:
const arr = new Float64Array(1000)
let sum = 0
for (let i = 0; i < arr.length; i++) {
  sum += arr[i]  // Direct memory access — essentially C speed
}
```

Compare to regular Array: property lookup, element kind check, potential deopt.

### Endianness and DataView

```
x86 (little-endian) stores 0x01020304 as:
Memory: [04][03][02][01]

Some network protocols use big-endian (network byte order).
DataView handles both:
```

```javascript
const buf = new ArrayBuffer(4)
const view = new DataView(buf)

view.setUint32(0, 0x01020304, false)  // Big-endian (network order)
view.setUint32(0, 0x01020304, true)   // Little-endian (host order)

view.getUint8(0)  // Reads first byte (depends on endian choice)
```

## 🔁 Execution Flow — Transferable ArrayBuffer

```javascript
// Transfer ArrayBuffer to Worker (zero-copy)
const buffer = new ArrayBuffer(1024 * 1024)  // 1MB
// buffer.byteLength = 1024 * 1024 in main thread

worker.postMessage({ buffer }, [buffer])  // Transfer (not clone!)
// After transfer: buffer.byteLength = 0 in main thread!
// Worker receives the same memory — no copy

// vs. clone (non-transfer):
worker.postMessage({ buffer })  // Clones 1MB — slow!
// buffer.byteLength = 1024 * 1024 still in main thread (copy was sent)
```

## 🧠 Memory Behavior

```
Regular Array:   heap-managed, elements may be SMI/HeapObject
TypedArray:      backing store in separate allocator (C++ heap)
                 V8 tracks via ExternalMemory → affects GC scheduling

Memory lifecycle:
1. new ArrayBuffer(n) → allocates n bytes in C++ allocator
2. JSArrayBuffer created in V8 heap
3. AdjustExternalMemory(+n) → tells V8 GC about n bytes of external memory
4. JSArrayBuffer becomes unreachable → GC scheduled
5. GC runs → JSArrayBuffer finalized → backing store freed
6. AdjustExternalMemory(-n)

Key insight: 
- 100MB ArrayBuffer: JSArrayBuffer is tiny (~50 bytes) in V8 heap
- But V8 still knows about the 100MB via ExternalMemory tracking
- This is why process.memoryUsage().external grows with ArrayBuffers
```

## 📐 ASCII Diagram — TypedArray Views

```
ArrayBuffer (16 bytes):
[00][01][02][03][04][05][06][07][08][09][10][11][12][13][14][15]

Int32Array (byteOffset=0, length=4):
[───int0────] [───int1────] [───int2────] [───int3────]

Uint8Array (byteOffset=0, length=16):
[u0][u1][u2][u3][u4][u5][u6][u7][u8][u9][uA][uB][uC][uD][uE][uF]

Float32Array (byteOffset=4, length=2):  [OFFSET into buffer]
              [──── f0 ─────] [──── f1 ─────]

Multiple views can overlay the SAME buffer simultaneously
```

## 🔍 Code Examples

### Example 1 — Binary Protocol Parsing

```javascript
// Parse a binary message header:
// [version: 1 byte][type: 1 byte][length: 4 bytes BE][payload: N bytes]

function parseMessage(buffer) {
  const view = new DataView(buffer)
  const version = view.getUint8(0)
  const type = view.getUint8(1)
  const payloadLength = view.getUint32(2, false)  // Big-endian!
  
  const payload = new Uint8Array(buffer, 6, payloadLength)
  
  return { version, type, payload }
}

// Create binary message:
function createMessage(type, payload) {
  const buffer = new ArrayBuffer(6 + payload.byteLength)
  const view = new DataView(buffer)
  view.setUint8(0, 1)            // version = 1
  view.setUint8(1, type)
  view.setUint32(2, payload.byteLength, false)
  new Uint8Array(buffer, 6).set(payload)
  return buffer
}
```

### Example 2 — WebGL Vertex Buffer

```javascript
// WebGL: all geometry data must be TypedArrays
const vertices = new Float32Array([
  // x,    y,    z,    r,   g,   b
  -0.5, -0.5,  0.0,  1.0, 0.0, 0.0,
   0.5, -0.5,  0.0,  0.0, 1.0, 0.0,
   0.0,  0.5,  0.0,  0.0, 0.0, 1.0,
])

const vbo = gl.createBuffer()
gl.bindBuffer(gl.ARRAY_BUFFER, vbo)
gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW)
// vertices memory is sent to GPU — zero additional copy from Float32Array
```

### Example 3 — SharedArrayBuffer for Worker Communication

```javascript
// main.js
const sharedBuffer = new SharedArrayBuffer(4 * 1000)  // 1000 Float32 values
const shared = new Float32Array(sharedBuffer)

// Fill with sensor data
for (let i = 0; i < 1000; i++) shared[i] = readSensor(i)

const worker = new Worker('./processor.js')
worker.postMessage({ buffer: sharedBuffer })  // No copy! Same memory

// worker.js
onmessage = ({ data }) => {
  const shared = new Float32Array(data.buffer)
  // Process in-place: no serialization overhead
  for (let i = 0; i < shared.length; i++) {
    shared[i] = transform(shared[i])
  }
  postMessage('done')
}
```

### Example 4 — Memory-Efficient Image Processing

```javascript
// Process RGBA image data without extra allocations
function invertColors(imageData) {
  const { data } = imageData  // Uint8ClampedArray — backed by canvas buffer
  
  // Direct memory manipulation — fastest possible
  for (let i = 0; i < data.length; i += 4) {
    data[i]     = 255 - data[i]     // R
    data[i + 1] = 255 - data[i + 1] // G
    data[i + 2] = 255 - data[i + 2] // B
    // data[i + 3]: Alpha — leave unchanged
  }
  
  return imageData
}

// SIMD optimization potential (using WebAssembly for even more speed):
// Process 16 bytes at once with 128-bit SIMD instructions
// 4x speedup on supported hardware
```

## 💥 Production Failures

### Failure — ArrayBuffer Detachment After Transfer

```javascript
const buffer = new ArrayBuffer(1024)
const view = new Uint8Array(buffer)

// Transfer to worker
worker.postMessage(buffer, [buffer])

// Accessing detached buffer:
view[0]  // TypeError: Cannot perform %TypedArray%.prototype.get
         // on a detached ArrayBuffer
buffer.byteLength  // 0 — buffer is detached

// Fix: always check or transfer separate from any existing views
// Create view AFTER receiving in worker, not before transfer
```

### Failure — Large ArrayBuffer OOM

```javascript
// Allocating large ArrayBuffers: fails silently on some platforms
try {
  const huge = new ArrayBuffer(8 * 1024 * 1024 * 1024)  // 8GB
} catch(e) {
  // RangeError: Invalid typed array length
  // or: Out of memory
}

// Browser limit: typically 2GB per ArrayBuffer (varies)
// Node.js: limited by process memory + swap

// Check available memory before large allocation:
const { heapTotal, external } = process.memoryUsage()
// But external memory (TypedArrays) doesn't show in heapUsed!
```

## ⚠️ Edge Cases

### Uint8ClampedArray vs Uint8Array

```javascript
const clamped = new Uint8ClampedArray(1)
const regular = new Uint8Array(1)

clamped[0] = 300  // Clamped to 255 (not overflow)
regular[0] = 300  // Overflows: stores 300 % 256 = 44

// Uint8ClampedArray used for: canvas ImageData, CSS colors
// Uint8Array used for: general binary, network data
```

### Negative Indices Not Supported

```javascript
const arr = new Int32Array(5)
arr[-1]  // undefined (not supported like Array.at(-1))
arr.at(-1)  // Works! TypedArrays have .at() method (ES2022)
```

## 🏢 Industry Best Practices

1. **Use TypedArrays for all binary data** — WebSockets, WebRTC data channels, file reading.
2. **Transfer instead of clone** — Always use transfer list in postMessage for large buffers.
3. **Reuse ArrayBuffers** — Allocation is cheap but tracking/GC has overhead. Pool buffers for frequently allocated/freed data.
4. **Use DataView for protocol parsing** — Correct endian handling; TypedArray endianness is platform-dependent.
5. **Monitor external memory** — `process.memoryUsage().external` tracks TypedArray backing stores.

## ⚖️ Trade-offs

| Type | Performance | Flexibility | Use Case |
|------|------------|-------------|---------|
| TypedArray | Fastest (typed, fixed) | Low (one type) | Homogeneous data, graphics |
| DataView | Medium (any type) | High | Protocol parsing, mixed types |
| Regular Array | Slower (untyped) | Highest | General JS values |
| SharedArrayBuffer | Fast (zero-copy) | Medium | Multi-threaded computation |

## 💼 Interview Questions

**Q1: Why is TypedArray element access faster than regular Array element access?**
> TypedArrays have a fixed element type known at construction time. V8 can generate specialized machine code that directly reads/writes from the backing store memory at computed byte offsets — essentially `*(base_ptr + index * element_size)`. Regular arrays can hold mixed types (SMI, HeapObject, undefined, holes) requiring element kind checks and potentially heap object dereferencing. TypedArray access is essentially a bounds check + memory load.

**Q2: What happens to an ArrayBuffer when transferred to a Worker?**
> The backing store's ownership is transferred to the worker's V8 Isolate. The original `ArrayBuffer` object in the main thread becomes "detached" — its backing store pointer is set to null and `byteLength` becomes 0. Any TypedArray views created from it in the main thread also become detached. The worker receives a new `ArrayBuffer` object wrapping the same memory. No bytes are copied — this is a zero-copy transfer.

## 🔗 Navigation

**Prev:** [11_Symbols_and_Iterators.md](11_Symbols_and_Iterators.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [../Browser/01_DOM_Manipulation.md](../Browser/01_DOM_Manipulation.md)
