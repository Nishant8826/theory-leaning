# Streams Basics

If you read a large file (like a 2GB log file or video export) into memory using standard file APIs, your application will crash with an Out of Memory error. Streams allow you to process data chunk-by-chunk as it arrives from the operating system or network, keeping your application's memory footprint low (often just a few megabytes) regardless of file size.

### What is a Stream?
A **Stream** is an abstract interface in Node.js for working with streaming data. Instead of loading an entire file or network response into memory all at once, streams read and write data in small, sequential chunks.

### The Four Stream Types
1. **Readable Streams**: Sources of data that you can read from (e.g., `fs.createReadStream`, `http.IncomingMessage`).
2. **Writable Streams**: Destinations that you can write data to (e.g., `fs.createWriteStream`, `http.ServerResponse`).
3. **Duplex Streams**: Streams that are both Readable and Writable (e.g., a network socket `net.Socket`).
4. **Transform Streams**: A type of Duplex stream that can modify or transform the data as it is written and read (e.g., `zlib.createGzip` for compression).

### Piping
**Piping** is the process of connecting the output of a Readable stream directly to the input of a Writable stream. It automates the flow of data, ensuring that the destination stream is not overwhelmed by the source stream.

```javascript
readableStream.pipe(writableStream);
```

## Deep Dive

### Memory Efficiency: Buffer vs. Stream
* **Buffer Approach**: Reading a 50MB file loads all 50MB into V8 heap memory at once. If 100 users request this file concurrently, the server allocates 5GB of memory, which can exhaust resources and cause crash cascades.
* **Stream Approach**: Reading a 50MB file splits the data into small chunks (usually 64KB by default). The server reads a chunk, sends it to the client, and discards it from memory before reading the next chunk. The memory usage remains flat at ~64KB per request, allowing the server to handle many more concurrent requests.

## Visual Explanation

### Processing Large Datasets: Buffer vs. Stream
```text
Buffer Approach (High Memory Cost):
[ File on Disk (50MB) ] ── Loaded all at once ──> [ V8 Memory Heap (50MB) ] ── Send to ──> [ Client ]

Stream Approach (Flat Memory Cost):
[ File on Disk (50MB) ]
   │
   ├── [ Chunk 1 (64KB) ] ──> [ RAM (64KB) ] ──> [ Client ] ──> (Free memory)
   ├── [ Chunk 2 (64KB) ] ──> [ RAM (64KB) ] ──> [ Client ] ──> (Free memory)
   └── [ Chunk 3 (64KB) ] ──> [ RAM (64KB) ] ──> [ Client ] ──> (Free memory)
```

## Real-World Example
Consider an API endpoint that compresses large log files. Using the buffer approach, the server must read the file into memory, run compression in memory, and then write it back to disk. Using streams, you can pipe a readable file stream through a Gzip transform stream directly into a writeable file stream, compressing the file in real-time with minimal memory usage.

## Code Examples

### Buffer vs. Stream Execution Comparison

```javascript
// stream-comparison.js
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

const sourceFile = path.join(__dirname, 'input.txt');
const destFile = path.join(__dirname, 'output.gz');

// Create a dummy file containing sample text (approx 5MB)
const fileWrite = fs.createWriteStream(sourceFile);
for (let i = 0; i < 100000; i++) {
  fileWrite.write('Node.js streams are highly memory-efficient backend construct.\n');
}
fileWrite.end();

fileWrite.on('finish', () => {
  console.log('Dummy file created. Commencing stream processing...');

  // 1. Create Readable stream (default chunk size: 64KB)
  const readStream = fs.createReadStream(sourceFile);

  // 2. Create Transform stream (Gzip compression)
  const gzipStream = zlib.createGzip();

  // 3. Create Writable stream (write to disk)
  const writeStream = fs.createWriteStream(destFile);

  // Measure initial memory
  const initialMemory = process.memoryUsage().heapUsed;

  // Pipe streams together: Read -> Gzip -> Write
  readStream
    .pipe(gzipStream)
    .pipe(writeStream)
    .on('finish', () => {
      const finalMemory = process.memoryUsage().heapUsed;
      const memoryDiff = ((finalMemory - initialMemory) / 1024 / 1024).toFixed(2);
      
      console.log(`Stream pipeline completed.`);
      console.log(`Memory consumed during execution: ${memoryDiff} MB`);
      
      // Cleanup files
      fs.unlinkSync(sourceFile);
      fs.unlinkSync(destFile);
    });
});
```

## Best Practices
* **Use Streams for Large Files**: Always use streams for processing files, HTTP payloads, or database records that can grow larger than a few megabytes.
* **Listen for Errors**: Always attach error listeners (`.on('error', callback)`) to all streams in a pipeline to prevent unhandled exceptions from crashing your process.
* **Avoid Mixing Methods**: Do not mix streaming and buffering APIs (e.g. do not read a file using a stream and then push the chunks into a single large array memory buffer).

## Interview Questions

**Q:** What is a stream in Node.js, and what is its primary benefit?

> **Answer:**
> A stream is an interface in Node.js for reading or writing data chunk-by-chunk. Its primary benefit is memory efficiency, allowing you to process large files or network payloads without loading the entire dataset into memory at once.

**Q:** Name the four main types of streams and provide a real-world example of each.

> **Answer:**
> 1. **Readable**: Source of data (e.g., `fs.createReadStream` to read files).
> 2. **Writable**: Destination for data (e.g., `fs.createWriteStream` to write files).
> 3. **Duplex**: Can both read and write (e.g., `net.Socket` to communicate over TCP).
> 4. **Transform**: Modifies data as it passes through (e.g., `zlib.createGzip` to compress files).

**Q:** What does the `.pipe()` method do, and how does it help manage stream speed differences?

> **Answer:**
> The `.pipe()` method connects the output of a Readable stream to the input of a Writable stream. It automatically manages the flow of data so that a fast Readable stream does not overwhelm a slow Writable stream (a condition known as **backpressure**). If the destination stream cannot keep up, `.pipe()` pauses the source stream until the destination is ready to receive more data.

**Q:** Discuss the potential memory risks when using `.pipe()` in Node.js without attaching error handlers. How does the modern `stream.pipeline` API solve these risks?

> **Answer:**
> The `.pipe()` method does not automatically clean up or destroy streams if an error occurs. If an error is thrown in the middle of a chain (e.g. `source.pipe(transform).pipe(dest)`), the streams remain open in memory, leading to file descriptor leaks and memory leaks.
> 
> To solve this, modern Node.js introduces `stream.pipeline()`. This utility function pipes streams together and automatically destroys all streams in the chain if any of them errors or closes. It also accepts a callback at the end to handle errors in a single location, making it the standard choice for production stream pipelines:
> ```javascript
> const { pipeline } = require('stream');
> pipeline(source, transform, dest, (err) => {
> if (err) console.error('Pipeline failed:', err);
> else console.log('Pipeline succeeded');
> });
> ```

---
Previous : [16_Buffers.md](16_Buffers.md) | Index : [00_index.md](00_index.md) | Next : [18_Callbacks.md](18_Callbacks.md)
