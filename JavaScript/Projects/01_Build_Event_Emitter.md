# 📌 Project 01 — Build an Event Emitter

## 🌟 Introduction

The **EventEmitter** is the heart of Node.js. It’s what allows parts of your app to "shout" (emit) an event and other parts to "listen" (on) and react.

In this project, we will build one from scratch using just plain JavaScript.

---

## 🏗️ 1. The Strategy

How do we remember who is listening to what? We use an **Object** as a registry:
-   **Keys:** The name of the event (e.g., `'click'`, `'data'`).
-   **Values:** An **Array** of functions that should run when that event happens.

---

## 🏗️ 2. The Implementation

```javascript
class MyEventEmitter {
  constructor() {
    this._events = {}; // Our registry: { eventName: [fn1, fn2] }
  }

  // 1. Subscribe
  on(name, listener) {
    if (!this._events[name]) {
      this._events[name] = [];
    }
    this._events[name].push(listener);
  }

  // 2. Emit (Trigger)
  emit(name, ...args) {
    if (!this._events[name]) return;
    
    // Run every function in the array
    this._events[name].forEach(listener => {
      listener(...args);
    });
  }

  // 3. Unsubscribe
  off(name, listenerToRemove) {
    if (!this._events[name]) return;

    this._events[name] = this._events[name].filter(listener => {
      return listener !== listenerToRemove;
    });
  }

  // 4. Subscribe for one-time only
  once(name, listener) {
    const wrapper = (...args) => {
      listener(...args);
      this.off(name, wrapper); // Remove self after one run
    };
    this.on(name, wrapper);
  }
}
```

---

## 🚀 3. Testing Your Emitter

```javascript
const bus = new MyEventEmitter();

const sayHello = (name) => console.log(`Hello, ${name}!`);

bus.on('greet', sayHello);
bus.emit('greet', 'Nishant'); // Output: Hello, Nishant!

bus.off('greet', sayHello);
bus.emit('greet', 'Nishant'); // (Nothing happens)
```

---

## 📐 Visualizing the Registry

```javascript
// Internal state of the object:
{
  "user_login": [ fn1, fn2 ],
  "data_error": [ fn3 ],
  "logout": []
}
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### Hidden Class Bloat
If you create thousands of different event names dynamically, the `this._events` object will keep growing and changing shape. This can turn the object into "Dictionary Mode" (slow). In the real Node.js source code, they use several optimizations (like using `Object.create(null)`) to ensure the registry stays as fast as possible even with thousands of events.

---

## 💼 Interview Tips

-   **Why use `...args`?** Because you don't know how many arguments the event will send (could be 1, could be 10).
-   **The `once` trick:** The key to `once` is creating a "wrapper" function that calls the original listener and then immediately calls `off()` on itself.
-   **Error Handling:** In a real-world emitter, you should wrap the `listener(...args)` in a `try...catch` block so that one broken listener doesn't crash the whole event bus.

---

## ⚖️ Trade-offs

| Feature | Simple Version | Production Version |
| :--- | :--- | :--- |
| **Max Listeners** | Unlimited (risks memory leaks). | Warns if you add >10 listeners. |
| **Error Handling** | None (one crash stops all). | Isolated (one crash doesn't affect others). |
| **Performance** | Basic array filtering. | Optimized linked lists or map lookups. |

---

## 🔗 Navigation

**Index:** [../00_Index.md](../00_Index.md) | **Next:** [02_Build_Promise.md](02_Build_Promise.md)
