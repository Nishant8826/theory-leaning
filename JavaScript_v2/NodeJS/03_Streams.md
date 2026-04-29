# 📌 03 — Streams

## 🧠 Concept Explanation

Node.js streams are an abstraction for reading/writing data in chunks — essential for handling large files, network data, and real-time processing without loading everything into memory. Streams implement backpressure: a mechanism to slow the producer when the consumer can't keep up.

**Stream types:**
- **Readable** — Source of data (fs.createReadStream, http.IncomingMessage)
- **Writable** — Destination (fs.createWriteStream, http.ServerResponse)
- **Duplex** — Both readable and writable (TCP socket, net.Socket)
- **Transform** — Duplex that transforms data (zlib, crypto ciphers, csv-parse)
- **PassThrough** — Transform that doesn't change data (for piping intermediaries)

## 🔬 Internal Mechanics

### Buffering and highWaterMark

Each stream has a **highWaterMark (HWM)** — the buffer size threshold:
- Readable: HWM is the target amount to buffer ahead
- Writable: HWM is the maximum internal buffer before backpressure kicks in

When `writable.write(chunk)` returns `false`: the internal buffer exceeds HWM — **stop writing!** Resume when `drain` event fires.

Ignoring backpressure = unbounded memory growth!

### Object Mode

Normal streams operate on Buffers/strings. Object mode (`{ objectMode: true }`) allows any JavaScript object as a chunk. Used for object streams in data pipelines (csv parsing → object transformation → db insert).

## 🔍 Code Examples

### Example 1 — Backpressure Implementation

```javascript
const { createReadStream, createWriteStream } = require('fs')

// WRONG: Ignores backpressure
const rs = createReadStream('huge-file.bin')
const ws = createWriteStream('output.bin')

rs.on('data', chunk => {
  ws.write(chunk)  // May return false! But we ignore it
  // ws internal buffer grows unboundedly → OOM
})

// CORRECT: Handle backpressure manually
rs.on('data', chunk => {
  const canContinue = ws.write(chunk)
  if (!canContinue) {
    rs.pause()  // Stop reading until ws drains
    ws.once('drain', () => rs.resume())
  }
})
rs.on('end', () => ws.end())

// BEST: Use pipe() — handles backpressure automatically
createReadStream('huge-file.bin').pipe(createWriteStream('output.bin'))
```

### Example 2 — Transform Stream

```javascript
const { Transform } = require('stream')

class JSONLineParser extends Transform {
  constructor(options = {}) {
    super({ ...options, objectMode: true })
    this._buffer = ''
  }
  
  _transform(chunk, encoding, callback) {
    this._buffer += chunk.toString()
    
    const lines = this._buffer.split('\n')
    this._buffer = lines.pop()  // Last (possibly incomplete) line
    
    for (const line of lines) {
      if (!line.trim()) continue
      try {
        this.push(JSON.parse(line))  // Push parsed object
      } catch(e) {
        this.destroy(new Error(`JSON parse error: ${e.message}`))
        return
      }
    }
    
    callback()  // Signal ready for more data
  }
  
  _flush(callback) {
    // Process remaining buffer at end of stream
    if (this._buffer.trim()) {
      try {
        this.push(JSON.parse(this._buffer))
      } catch(e) {
        this.destroy(new Error(`JSON flush error: ${e.message}`))
        return
      }
    }
    callback()
  }
}

// Usage:
createReadStream('data.jsonl')
  .pipe(new JSONLineParser())
  .on('data', (obj) => {
    processRecord(obj)
  })
```

### Example 3 — Async Iteration (Modern Stream Pattern)

```javascript
const { createReadStream } = require('fs')
const { createGunzip } = require('zlib')
const { pipeline } = require('stream/promises')

// Modern: async iteration over streams
async function processLargeFile(filePath) {
  const stream = createReadStream(filePath)
    .pipe(createGunzip())  // Decompress in-flight
  
  let lineBuffer = ''
  let count = 0
  
  for await (const chunk of stream) {
    lineBuffer += chunk.toString()
    const lines = lineBuffer.split('\n')
    lineBuffer = lines.pop()
    
    for (const line of lines) {
      await processLine(line)  // Awaiting is safe — backpressure respected
      count++
    }
  }
  
  return count
}

// pipeline() utility: proper error handling and cleanup
await pipeline(
  createReadStream('input.csv'),
  createGunzip(),
  new CSVParser(),
  new DataTransformer(),
  createWriteStream('output.json')
)
// pipeline(): handles errors in any stage, ensures cleanup of all streams
// stream.pipe() does NOT propagate errors!
```

## 💥 Production Failures

### Failure — pipe() Doesn't Propagate Errors

```javascript
// WRONG: pipe() doesn't propagate stream errors
fs.createReadStream('file.txt')
  .pipe(someTransform)
  .pipe(fs.createWriteStream('out.txt'))

// If createReadStream emits 'error': someTransform NOT destroyed!
// someTransform continues waiting for input that never comes
// Resource leak: file handles, transform state

// CORRECT: Use stream.pipeline() or explicit error handling
const { pipeline } = require('stream/promises')
try {
  await pipeline(
    fs.createReadStream('file.txt'),
    someTransform,
    fs.createWriteStream('out.txt')
  )
} catch(err) {
  console.error('Pipeline failed:', err)
  // All streams automatically destroyed by pipeline()
}
```

## 🏢 Industry Best Practices

1. **Use `stream.pipeline()`** instead of `.pipe()` for error handling.
2. **Respect backpressure** — Always handle `write()` returning `false`.
3. **Set appropriate HWM** — Default is 16KB for bytes, 16 objects for objectMode.
4. **Destroy on error** — Ensure streams are destroyed when errors occur.
5. **Use `for await...of`** for consuming readable streams in modern Node.js.

## 💼 Interview Questions

**Q1: What is backpressure and why does it matter?**
> Backpressure is the mechanism by which a writable stream signals to a readable stream to slow down when its internal buffer exceeds the highWaterMark. Without it, a fast producer (e.g., fast file read) fills the writable buffer unboundedly, consuming gigabytes of RAM. `writable.write()` returns `false` when backpressure is needed; `drain` event fires when ready. `pipe()` handles this automatically. Custom implementations must respect the return value of `write()`.

## 🔗 Navigation

**Prev:** [02_Event_Emitter.md](02_Event_Emitter.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [04_Cluster_Module.md](04_Cluster_Module.md)
