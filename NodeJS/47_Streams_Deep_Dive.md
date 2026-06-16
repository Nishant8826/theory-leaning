# Streams Deep Dive

While piping streams using `.pipe()` works for simple tasks, writing custom streams or handling high-throughput pipelines requires understanding stream internals. If you do not manage backpressure, a fast data source can overwhelm a slow data destination, causing the application to accumulate data in memory buffers, resulting in memory leaks and crashes.

### HighWaterMark and Backpressure
* **`highWaterMark`**: The maximum size (in bytes for binary streams, or count for object streams) of the internal buffer that a stream holds. The default is 16KB for standard streams and 64KB for filesystem streams.
* **Backpressure**: The mechanism that pauses a Readable stream when a Writable stream's internal buffer is full, preventing memory exhaustion.

When you call `writable.write(chunk)`, it returns a boolean value:
* **`true`**: The internal buffer is below the `highWaterMark`; you can write more data.
* **`false`**: The internal buffer has exceeded the `highWaterMark`. You must stop writing immediately and wait for the Writable stream to emit the **`drain`** event before writing more data.

## Deep Dive

### Implementing Custom Streams
To build custom streams, inherit from Node's native `stream` classes and implement their internal methods:
1. **Readable**: Implement `_read(size)`. Call `this.push(chunk)` to add data to the buffer, or `this.push(null)` to indicate the end of the stream.
2. **Writable**: Implement `_write(chunk, encoding, callback)`. Call `callback(err)` when you finish processing the chunk to signal that the stream is ready for the next one.
3. **Transform**: Implement `_transform(chunk, encoding, callback)`. Call `this.push(transformedChunk)` to output the modified data, and then call `callback()` to continue.

### Object Mode
By default, streams only handle binary buffers or text strings. Setting **`objectMode: true`** allows you to stream raw JavaScript objects, which is useful for processing database records or API payloads in chunks.

## Visual Explanation

### Backpressure Control Loop
```text
  [ Readable Stream ] ── push() ──> [ Internal Buffer (highWaterMark reached) ]
                                                   │
                                                   ▼ (returns false on write)
  [ Paused Readable ] <── stop writing ────────────┘
         │
         ▼ (Writable processes chunks from buffer)
  [ Writable Stream ] ── writes to disk ──> [ Buffer cleared ] ──> Emits 'drain' event
                                                                        │
  [ Readable Resumes ] <── resumes writing <────────────────────────────┘
```

## Real-World Example
Consider an application that exports millions of database records to a CSV file. If you query all records into memory at once, the application will crash. Using streams, you can create a custom database reader in `objectMode`, pipe the records through a Transform stream that formats them to CSV text, and write them directly to a file, processing millions of records with minimal memory usage.

## Code Examples

### Custom Streams, Backpressure Management, and ObjectMode

```javascript
// custom-streams-demo.js
const { Readable, Writable, Transform, pipeline } = require('stream');

// 1. Custom Readable Stream (Streams numbers from start to max)
class NumberSourceStream extends Readable {
  constructor(maxNumber, options = {}) {
    super({ ...options, objectMode: true }); // Enable objectMode to stream numbers directly
    this.current = 1;
    this.max = maxNumber;
  }

  // Must implement _read method
  _read() {
    if (this.current <= this.max) {
      this.push(this.current);
      this.current++;
    } else {
      this.push(null); // Signal End of Stream (EOF)
    }
  }
}

// 2. Custom Transform Stream (Squares input numbers and converts to string)
class SquareTransformStream extends Transform {
  constructor(options = {}) {
    // Convert objectMode input to string/buffer output
    super({
      ...options,
      writableObjectMode: true, // Input is JavaScript objects (numbers)
      readableObjectMode: false  // Output is binary/strings (text lines)
    });
  }

  // Must implement _transform method
  _transform(chunk, encoding, callback) {
    const squared = chunk * chunk;
    const outputString = `Number: ${chunk} | Squared: ${squared}\n`;
    this.push(outputString);
    callback(); // Ready for next chunk
  }
}

// 3. Custom Writable Stream with Backpressure simulation
class SlowWriteDestination extends Writable {
  constructor(options = {}) {
    super({ ...options, highWaterMark: 64 }); // Small buffer limit to trigger backpressure
  }

  // Must implement _write method
  _write(chunk, encoding, callback) {
    // Simulate slow disk write latency (50ms)
    setTimeout(() => {
      console.log(`[SLOW-WRITE] Processed bytes: ${chunk.length}`);
      callback(); // Signals that chunk was written
    }, 50);
  }
}

// 4. Run the Pipeline securely
const runPipeline = () => {
  const source = new NumberSourceStream(10);
  const transform = new SquareTransformStream();
  const destination = new SlowWriteDestination();

  pipeline(source, transform, destination, (err) => {
    if (err) {
      console.error('Pipeline failed with error:', err.message);
    } else {
      console.log('Pipeline successfully completed processing.');
    }
  });
};
runPipeline();
```

## Best Practices
* **Always Use `stream.pipeline`**: Do not chain streams using `.pipe()` in production. Use `stream.pipeline()` to ensure that all streams are cleaned up and file descriptors are closed if an error occurs.
* **Monitor `writable.write()` Returns**: When writing custom data producers, always check if `.write()` returns `false`. If it does, stop writing and wait for the `drain` event before continuing.
* **Define Proper `highWaterMark` Limits**: Adjust `highWaterMark` values based on your server resources. Setting it too high consumes memory; setting it too low increases context-switching latency.

## Interview Questions

**Q:** What is the difference between `.pipe()` and `stream.pipeline()`?

> **Answer:**
> `.pipe()` connects a Readable stream to a Writable stream but does not handle errors or clean up resources automatically if one of the streams fails. `stream.pipeline()` handles errors in a single location and automatically destroys all streams in the chain if an error occurs, preventing resource leaks.

**Q:** What is Backpressure in Node.js streams and how does the runtime handle it?

> **Answer:**
> Backpressure is a flow-control mechanism that occurs when a Writable stream cannot write data as fast as a Readable stream is sending it. When the Writable stream's internal buffer (`highWaterMark`) is full, `.write()` returns `false`. The event loop pauses the Readable stream until the Writable stream clears its buffer and emits a `'drain'` event, resuming the flow.

**Q:** Explain how `objectMode` works in Node.js streams and how the `highWaterMark` option behaves differently when it is enabled.

> **Answer:**
> By default, streams only accept binary buffers or strings. Setting `objectMode: true` allows streams to accept raw JavaScript objects.
> When `objectMode` is disabled, the `highWaterMark` limit is measured in **bytes** (defaulting to 16KB). When `objectMode` is enabled, the `highWaterMark` limit is measured in the **number of objects** (defaulting to 16 objects), regardless of the memory size of each object.

**Q:** How would you build a custom transform stream that parses high-throughput JSON logs, extracts specific keys, and gzip-compresses the output in a memory-bounded pipeline?

> **Answer:**
> To build this transform stream:
> 1. Inherit from the `Transform` class.
> 2. Configure `writableObjectMode: false` (to accept raw byte chunks) and `readableObjectMode: false` (to output binary compressed chunks).
> 3. Implement the `_transform` method:
> - Accumulate chunks until a complete JSON line delimiter is found.
> - Parse the JSON string: `const log = JSON.parse(line)`.
> - Extract the required fields, format them as a string, and pass the string to the next stream using `this.push(formattedString)`.
> 4. Use `stream.pipeline()` to connect a file read stream, your custom parser transform, a `zlib.createGzip()` transform, and a file write stream. This pipeline automatically manages backpressure and cleans up all stream resources if an error occurs.

---
Previous : [46_Event_Loop_Deep_Dive.md](46_Event_Loop_Deep_Dive.md) | Index : [00_index.md](00_index.md) | Next : [48_Worker_Threads.md](48_Worker_Threads.md)
