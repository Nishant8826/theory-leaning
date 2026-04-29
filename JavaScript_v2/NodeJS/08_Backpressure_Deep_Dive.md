# 📌 08 — Backpressure Deep Dive

## 🧠 Concept Explanation

Backpressure is the mechanism that prevents a fast producer from overwhelming a slow consumer. Without it, data buffers grow unboundedly in memory until the process runs out of RAM.

Backpressure appears at multiple layers:
- **Stream backpressure** — `writable.write()` returns false when buffer full
- **TCP backpressure** — OS network stack's receive window fills, slowing sender
- **HTTP/2 flow control** — Frame-level flow control for multiplexed streams
- **Queue backpressure** — Message queues (Kafka, RabbitMQ) apply back-pressure to producers

## 🔬 Internal Mechanics

### Node.js Stream Buffer Math

```
Readable stream:
  highWaterMark = 64KB (default)
  _readableState.length = current buffered bytes
  
  When _readableState.length > HWM:
    → readable.read() stops calling _read() (pauses reading)
    
Writable stream:
  highWaterMark = 16KB (default)
  _writableState.length = current buffered bytes
  
  When _writableState.length > HWM:
    → writable.write() returns false (signal backpressure)
    
  When _writableState.length == 0 and no pending writes:
    → 'drain' event emitted
```

## 🔍 Code Examples

### Example 1 — Custom Backpressure

```javascript
class RateLimitedWriter {
  constructor(writable, rateHz = 1000) {
    this.writable = writable
    this.interval = 1000 / rateHz
    this.queue = []
    this.processing = false
  }
  
  async write(data) {
    return new Promise((resolve, reject) => {
      this.queue.push({ data, resolve, reject })
      if (!this.processing) this.process()
    })
  }
  
  async process() {
    this.processing = true
    while (this.queue.length > 0) {
      const { data, resolve, reject } = this.queue.shift()
      
      const ok = this.writable.write(data)
      if (!ok) {
        await new Promise(resolve => this.writable.once('drain', resolve))
      }
      
      await new Promise(resolve => setTimeout(resolve, this.interval))
      resolve()
    }
    this.processing = false
  }
}
```

### Example 2 — Detecting Backpressure Violations

```javascript
function monitorStream(stream, name) {
  let writeCount = 0
  let drainCount = 0
  let backpressureViolations = 0
  
  const origWrite = stream.write.bind(stream)
  stream.write = function(chunk, ...args) {
    writeCount++
    const result = origWrite(chunk, ...args)
    if (!result) {
      backpressureViolations++
      // Someone called write() after it returned false!
    }
    return result
  }
  
  stream.on('drain', () => drainCount++)
  
  setInterval(() => {
    console.log(`[${name}] writes: ${writeCount}, drains: ${drainCount}, violations: ${backpressureViolations}`)
    writeCount = drainCount = backpressureViolations = 0
  }, 10000)
}
```

## 💥 Production Failure — Backpressure Ignored

```javascript
// Common WebSocket proxy backpressure bug
ws.on('message', (data) => {
  const ok = upstreamSocket.write(data)  // May return false!
  // We don't check the return value
  // If client sends fast and upstream is slow:
  // upstreamSocket buffer grows 1MB, 10MB, 100MB → OOM crash
})

// Fix:
ws.on('message', (data) => {
  const ok = upstreamSocket.write(data)
  if (!ok) {
    ws.pause()  // Stop receiving from client
    upstreamSocket.once('drain', () => ws.resume())
  }
})
```

## 🏢 Industry Best Practices

1. **Always check `write()` return value** — `false` means stop writing.
2. **Use `stream.pipeline()`** — Automatically manages backpressure across all streams.
3. **Set appropriate HWM** — Too small = too many drain events; too large = too much memory use.
4. **Monitor buffer sizes** — Alert if `writable._writableState.length > threshold`.
5. **Implement at every layer** — TCP, HTTP/2, application-level all need backpressure handling.

## 💼 Interview Questions

**Q1: How does TCP implement backpressure?**
> TCP uses a receive window: each side advertises how much buffer space it has. When the receiver's buffer fills (application not reading fast enough), it advertises a window of 0. The sender then must wait until the window opens. Node.js's writable streams mirror this pattern: `write()` returns false when the internal buffer exceeds HWM, signaling the application to stop writing. When the buffer drains, the `drain` event fires.

## 🔗 Navigation

**Prev:** [07_Event_Loop_Node_vs_Browser.md](07_Event_Loop_Node_vs_Browser.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [../Patterns/01_Module_Pattern.md](../Patterns/01_Module_Pattern.md)
