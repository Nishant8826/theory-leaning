# 📌 02 — EventEmitter

## 🌟 Introduction

In Node.js, things happen asynchronously. How does one part of your app know when another part has finished a task? They use the **EventEmitter**.

Think of it like a **Radio Station**:
-   **The Station (Emitter):** Shouts out news (Events) like "Song Started" or "Weather Update."
-   **The Radio (Listener):** You tune in to the station. When they shout "Weather Update," your radio reacts by playing the sound.

Nearly everything in Node.js (Streams, HTTP Servers, File Systems) uses the EventEmitter under the hood.

---

## 🏗️ Core Methods

1.  **`emit('event', data)`**: Sends a message to everyone listening.
2.  **`on('event', callback)`**: Starts listening for a specific message.
3.  **`once('event', callback)`**: Listens for the message **only once**, then stops.
4.  **`off('event', callback)`**: Stops listening entirely.

---

## 🏗️ The "Crash" Rule (Error Events)

The `error` event is special in Node.js.

> [!CAUTION]
> **If you `emit('error')` and there is no `.on('error')` listener attached, Node.js will crash your entire application.**

Always, always add an error listener to your emitters!

```javascript
const EventEmitter = require('events');
const myEmitter = new EventEmitter();

// ✅ ALWAYS DO THIS
myEmitter.on('error', (err) => {
  console.error('Whoops! There was an error:', err.message);
});

myEmitter.emit('error', new Error('Something went wrong'));
```

---

## 🚀 Memory Management & Leaks

By default, Node.js allows only **10 listeners** for a single event. If you add more, it will print a warning in your terminal.

**Why?** Because adding listeners usually creates a **Closure**. If you keep adding listeners without removing them, your app will slowly eat up all the RAM (a Memory Leak).

---

## 🔍 Code Walkthrough: A Simple Order System

```javascript
const EventEmitter = require('events');

class OrderSystem extends EventEmitter {
  placeOrder(item) {
    console.log(`Placing order for: ${item}`);
    // Shout to anyone listening!
    this.emit('order_placed', { item, time: Date.now() });
  }
}

const shop = new OrderSystem();

// Listener 1: Update Inventory
shop.on('order_placed', (data) => {
  console.log(`Inventory: Removing 1 ${data.item} from stock.`);
});

// Listener 2: Send Email
shop.on('order_placed', (data) => {
  console.log(`Email: Sending confirmation for ${data.item}.`);
});

shop.placeOrder('Laptop');
```

---

## 📐 Visualizing the Event Flow

```text
[ ORDER SYSTEM ] ─── (Emit: "Order Placed") ──▶ [ EVENT EMITTER ]
                                                     │
                                        ┌────────────┴────────────┐
                                        ▼                         ▼
                                 [ INVENTORY ]              [ EMAIL SYSTEM ]
                                 (Reacts...)                (Reacts...)
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### _events Object
Internally, the `EventEmitter` is just a plain JavaScript object called `_events`. When you call `shop.on('order', fn)`, Node.js adds your function to an array: `_events['order'] = [fn1, fn2]`. When you call `emit`, Node just loops through that array and calls every function. This is why it's very fast—it’s just a simple object lookup and a loop.

---

## 💼 Interview Questions

**Q1: Why does Node.js crash on unhandled 'error' events?**
> **Ans:** Node.js treats errors as critical. If you don't handle an error, Node assumes your app is in an unstable state and shuts it down to prevent further damage (like corrupting a database).

**Q2: What is the difference between `on()` and `once()`?**
> **Ans:** `on()` keeps listening for the event forever until you manually call `off()`. `once()` triggers the callback only the very first time the event happens, and then it automatically removes itself.

**Q3: How do you prevent a memory leak in an EventEmitter?**
> **Ans:** Always remove listeners when you are done with them using `.off()` or `.removeListener()`, especially inside repeating functions like HTTP request handlers.

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **EventEmitter** | Decouples code; very fast. | Hard to track the flow of data in large apps. |
| **Promises** | Clearer success/failure flow. | Can only resolve **once**. |
| **Streams** | Handles massive amounts of data. | Complex and harder to write. |

---

## 🔗 Navigation

**Prev:** [01_Node_Architecture.md](01_Node_Architecture.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [03_Streams.md](03_Streams.md)
