# 📌 12 — TypedArrays & ArrayBuffers

## 🌟 Introduction

Usually, JavaScript handles data in a very "user-friendly" way (Arrays and Objects). But sometimes, you need to handle **raw binary data** (0s and 1s) for high-performance tasks like:
-   **Image/Video Processing**
-   **Game Engines (WebGL)**
-   **Audio Processing**
-   **WebSockets (Network protocols)**

This is where **ArrayBuffers** and **TypedArrays** come in.

---

## 🏗️ The 2-Part System

To handle raw data, JavaScript uses two separate parts:

### 1. ArrayBuffer (The Memory)
This is a fixed-length "box" of raw bytes. You **cannot** read or write to it directly. It’s just the storage.

### 2. TypedArrays (The View)
To read or write to the box, you need a "View." A TypedArray acts like a pair of lenses that tells you how to interpret the bytes (as 8-bit integers, 32-bit floats, etc.).

```javascript
// 1. Create a "box" of 16 bytes
const buffer = new ArrayBuffer(16);

// 2. Create a "view" that sees the bytes as 32-bit integers
const view = new Int32Array(buffer);

view[0] = 100; // This takes up 4 bytes (32 bits)
console.log(view.length); // 4 (Since 16 bytes / 4 bytes per int = 4 items)
```

---

## 🚀 Common Types of Views

| View | Type | Size (Bytes) | Range |
| :--- | :--- | :--- | :--- |
| **Uint8Array** | Unsigned 8-bit Int | 1 | 0 to 255 |
| **Int16Array** | Signed 16-bit Int | 2 | -32,768 to 32,767 |
| **Float32Array** | 32-bit Float | 4 | Decimal numbers |
| **BigInt64Array** | 64-bit BigInt | 8 | Huge numbers |

---

## 📐 Visualizing the Buffer & Views

One buffer can have **multiple views** looking at it at the same time:

```text
ARRAY BUFFER (8 Bytes)
[ 0 ][ 1 ][ 2 ][ 3 ][ 4 ][ 5 ][ 6 ][ 7 ]

VIEW 1: Uint8Array (8 items)
[u][u][u][u][u][u][u][u]

VIEW 2: Int32Array (2 items)
[------- i1 -------][------- i2 -------]
```

---

## 🏎️ Performance Benefit

Regular JavaScript Arrays are "smart" and can grow or shrink, and hold different types of data (strings, numbers, objects). This makes them **slow**.

TypedArrays are "dumb" and fixed. Because they only hold one type of number, the CPU can process them at **lightning speed** (almost as fast as C or C++).

---

## 🔍 Code Walkthrough: Image Inversion

This is how a browser might process an image efficiently:

```javascript
function invertColors(pixels) {
  // pixels is a Uint8ClampedArray [R, G, B, A, R, G, B, A...]
  for (let i = 0; i < pixels.length; i += 4) {
    pixels[i]     = 255 - pixels[i];     // Invert Red
    pixels[i + 1] = 255 - pixels[i + 1]; // Invert Green
    pixels[i + 2] = 255 - pixels[i + 2]; // Invert Blue
    // pixels[i + 3] is Alpha (transparency), we leave it
  }
}
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### External Memory
In V8, the memory for an `ArrayBuffer` is allocated **outside** of the main V8 heap (where regular objects live). This is called **External Memory**. This prevents large binary files from cluttering up the main garbage collection cycle, making the rest of your app run more smoothly.

---

## 💼 Interview Questions

**Q1: What is the difference between an Array and a TypedArray?**
> **Ans:** A regular Array can hold mixed types and is dynamic in size. A TypedArray is fixed-length and can only hold one specific type of numeric data, making it much faster for math and binary processing.

**Q2: What is a DataView?**
> **Ans:** A `DataView` is a more flexible view that allows you to read/write different types of data (Int8, Float32, etc.) from the same buffer at arbitrary offsets.

**Q3: Can you change the size of an ArrayBuffer?**
> **Ans:** No. Once an `ArrayBuffer` is created, its size is fixed. To "resize" it, you must create a new buffer and copy the data over.

---

## ⚖️ Trade-offs

| Feature | Regular Array | TypedArray |
| :--- | :--- | :--- |
| **Ease of Use** | High (very flexible). | Low (requires views/buffers). |
| **Performance** | Good for general tasks. | Exceptional for math/binary. |
| **Memory** | High overhead. | Low, compact storage. |
| **Methods** | `push`, `pop`, `map`, etc. | No `push`/`pop` (fixed length). |

---

## 🔗 Navigation

**Prev:** [11_Symbols_and_Iterators.md](11_Symbols_and_Iterators.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [../Browser/01_DOM_Manipulation.md](../Browser/01_DOM_Manipulation.md)
