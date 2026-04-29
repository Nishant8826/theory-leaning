# 📌 03 — Streams

## 🌟 Introduction

Imagine you have a 10GB video file. If you try to open it using `fs.readFile`, Node.js will try to load the **entire file** into your RAM. Your computer will likely crash.

**Streams** solve this. They allow you to process data **piece by piece** (in "chunks") without loading it all at once.

Think of it like **Netflix**:
-   You don't wait for the whole movie to download before watching.
-   You watch the first minute while the second minute is still downloading. This is "streaming."

---

## 🏗️ The 4 Types of Streams

Node.js provides four fundamental stream types. Think of data as "water" flowing through pipes.

1.  **Readable Streams** (The Source 🚰)
    *   **What it does:** Allows you to read data piece-by-piece from a source.
    *   **Examples:** `fs.createReadStream()` (reading a file), `http.IncomingMessage` (receiving an HTTP request).
    *   **Analogy:** A water tap. You turn it on, and water (data) flows out for you to collect.

2.  **Writable Streams** (The Destination 🪣)
    *   **What it does:** Allows you to write data piece-by-piece to a destination.
    *   **Examples:** `fs.createWriteStream()` (writing to a file), `http.ServerResponse` (sending an HTTP response back to a user).
    *   **Analogy:** A bucket or a drain. You pour water (data) into it.

3.  **Duplex Streams** (Two-Way Communication ☎️)
    *   **What it does:** A stream that is both Readable and Writable simultaneously. The read and write channels are independent.
    *   **Examples:** `net.Socket` (a TCP network connection). You can send messages to a server and receive messages from it at the same time.
    *   **Analogy:** A telephone conversation. You can speak (write) and listen (read) at the same time, but your speech isn't what you are hearing.

4.  **Transform Streams** (The Modifier 🧊)
    *   **What it does:** A special type of Duplex stream where the output is directly computed from the input. It modifies or transforms the data as it passes through.
    *   **Examples:** `zlib.createGzip()` (compressing data into a zip), `crypto.createCipheriv()` (encrypting data for security).
    *   **Analogy:** A water filter. Dirty water enters (input), the filter processes it, and clean water comes out (output).

---

## 🚀 The Power of `.pipe()`

The `.pipe()` method is the easiest and most efficient way to consume streams in Node.js. It connects a **Readable stream** directly to a **Writable stream**, just like connecting pipes in plumbing.

### Why use `.pipe()`?
1. **Automatic Data Management:** It automatically listens for `'data'` and `'end'` events from the readable stream and writes them to the destination.
2. **Backpressure Handling:** If the Writable stream (e.g., a slow hard drive) cannot process data as fast as the Readable stream provides it, `.pipe()` will automatically pause the Readable stream until the Writable stream catches up. This prevents memory leaks and crashes!
3. **Chaining:** Because `.pipe()` returns the destination stream, you can chain multiple streams together easily (especially useful with Transform streams).

### The Syntax
```javascript
readableSource.pipe(writableDestination)
```

### Example: Compressing a File on the Fly
Here is how you can read a file, compress it, and write it to a new file, all without holding the whole file in memory:

```javascript
const fs = require('fs');
const zlib = require('zlib'); // Built-in compression tool

const readStream = fs.createReadStream('large-file.txt');
const writeStream = fs.createWriteStream('compressed.txt.gz');
const compress = zlib.createGzip(); // A Transform stream

// Read -> Compress -> Write
// Chaining: readStream pipes to compress, which pipes to writeStream
readStream.pipe(compress).pipe(writeStream);
```

---

## 📐 Visualizing the Stream Plumbing

The stream pipeline acts like a chain of pipes. Data flows through each "station" until it reaches the destination.

```text
 🚰 [ SOURCE ] ─────────▶ [ CHUNK ] ─────────▶ [ TRANSFORM ] ─────────▶ 🪣 [ DEST ]
 (e.g. 10GB File)         (64KB size)           (Gzip/Filter)          (Result File)
 
       │                                                                      ▲
       └───────────────────────── (BACKPRESSURE SIGNAL) ──────────────────────┘
                   "Stop! My internal buffer is full. Slow down!"
```

---

## 🛠️ Real-World Troubleshooting (Q&A)

**P1: "Memory usage is still high even with Streams."**
> **Problem:** You are reading from a fast source (like a local SSD) and writing to a slow destination (like a remote cloud API).
> **Reason:** If you don't handle **Backpressure**, Node.js will store the "unread" data in its RAM (the `highWaterMark` buffer). If the gap is huge, the buffer will keep growing until your app runs out of memory.
> **Fix:** Use `.pipe()` or `pipeline()` which handle backpressure automatically, or check if `write()` returns `false` before sending more data.

**P2: "My file is corrupted after streaming."**
> **Problem:** The destination file is missing data or has garbage values.
> **Reason:** You didn't handle the `finish` or `error` events correctly. You might have closed the file before the stream finished writing the last chunk.
> **Fix:** Use the `stream.pipeline()` utility. It ensures that if one stream fails, all of them are closed properly, and it provides a clean callback for when the whole process is done.

**P3: "Transform stream is not producing any output."**
> **Problem:** You sent data into a transform stream, but nothing comes out.
> **Reason:** You likely forgot to call the `callback()` inside your `_transform` method.
> **Fix:** Ensure every call to `_transform(chunk, encoding, callback)` eventually calls `callback(null, processedData)`.

---

## 🏗️ What is Backpressure?

Imagine a **fast tap** and a **small bucket**. If the tap stays on full speed, the bucket will overflow.

**Backpressure** is Node.js’s way of saying: "Hey Tap, slow down! The bucket is full. Wait for me to empty it before you send more."

---

## 🔬 Deep Technical Dive (V8 Internals)

### highWaterMark
Every stream has a property called `highWaterMark`. For binary streams, the default is **16KB**. This is the maximum amount of data Node.js will "buffer" (store in memory) before it starts applying backpressure.

---

## 💼 Interview Questions

**Q1: What is Backpressure?**
> **Ans:** It’s a protection mechanism. When a "Writable" stream is slower than a "Readable" stream, the Writable stream tells the Readable stream to pause so that the internal memory buffer doesn't overflow.

**Q2: Why use `stream.pipeline()` instead of `.pipe()`?**
> **Ans:** `.pipe()` does not handle errors well. `pipeline()` automatically handles errors and cleans up all streams if any of them fail.

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **Standard Pipe** | Simple and easy. | Terrible error handling. |
| **`pipeline()`** | Safe and production-ready. | Slightly more verbose. |
| **Async Iteration**| Very modern and clean. | Requires Node.js 12+. |

---

## 🔗 Navigation

**Prev:** [02_Event_Emitter.md](02_Event_Emitter.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [04_Cluster_Module.md](04_Cluster_Module.md)
