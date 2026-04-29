# 📌 Project 06 — Real-Time Chat System Design

## 🎯 Goal

Design and implement a WebSocket-based real-time chat system. This integrates event emitters, backpressure, connection management, and state synchronization.

## ✅ Server Implementation

```javascript
const WebSocket = require("ws")
const EventEmitter = require("events")

class ChatRoom extends EventEmitter {
  constructor(id) {
    super()
    this.id = id
    this.clients = new Map()  // userId → WebSocket
    this.history = []
    this.MAX_HISTORY = 100
  }
  
  join(userId, ws) {
    this.clients.set(userId, ws)
    
    // Send history to new client
    ws.send(JSON.stringify({ type: "HISTORY", messages: this.history.slice(-50) }))
    
    this.broadcast({ type: "JOIN", userId, timestamp: Date.now() }, userId)
    
    ws.on("message", (data) => this.handleMessage(userId, data))
    ws.on("close", () => this.leave(userId))
    ws.on("error", (err) => { console.error(err); this.leave(userId) })
  }
  
  leave(userId) {
    this.clients.delete(userId)
    this.broadcast({ type: "LEAVE", userId, timestamp: Date.now() })
  }
  
  handleMessage(userId, data) {
    let parsed
    try { parsed = JSON.parse(data) } catch { return }
    
    if (parsed.type === "MESSAGE") {
      const message = {
        id: generateId(),
        userId,
        text: sanitize(parsed.text),
        timestamp: Date.now()
      }
      
      this.history.push(message)
      if (this.history.length > this.MAX_HISTORY) this.history.shift()
      
      this.broadcast({ type: "MESSAGE", message })
    }
  }
  
  broadcast(data, excludeUserId = null) {
    const payload = JSON.stringify(data)
    
    this.clients.forEach((ws, userId) => {
      if (userId === excludeUserId) return
      if (ws.readyState !== WebSocket.OPEN) return
      
      // Check backpressure
      if (ws.bufferedAmount > 16384) {  // 16KB threshold
        console.warn(`Client ${userId} has ${ws.bufferedAmount} bytes buffered`)
        return  // Skip this client (don't accumulate messages)
      }
      
      ws.send(payload, (err) => {
        if (err) this.leave(userId)
      })
    })
  }
}

class ChatServer {
  constructor(port) {
    this.rooms = new Map()
    this.wss = new WebSocket.Server({ port })
    
    this.wss.on("connection", this.handleConnection.bind(this))
    
    // Cleanup dead connections
    setInterval(() => this.ping(), 30000)
  }
  
  handleConnection(ws, req) {
    const { userId, roomId } = parseQuery(req.url)
    
    ws.isAlive = true
    ws.on("pong", () => { ws.isAlive = true })
    
    if (!this.rooms.has(roomId)) {
      this.rooms.set(roomId, new ChatRoom(roomId))
    }
    
    this.rooms.get(roomId).join(userId, ws)
  }
  
  ping() {
    this.wss.clients.forEach(ws => {
      if (!ws.isAlive) return ws.terminate()
      ws.isAlive = false
      ws.ping()
    })
  }
}
```

## 🔗 Navigation

**Prev:** [05_Build_Rate_Limiter.md](05_Build_Rate_Limiter.md) | **Index:** [../00_Index.md](../00_Index.md)
