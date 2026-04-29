# 📌 05 — Strategy Pattern

## 🌟 Introduction

The **Strategy Pattern** is a way to change how an object behaves at runtime by "swapping out" its logic. It helps you avoid giant, messy `if/else` or `switch` statements.

Think of it like a **Gaming Console**:
-   The **Console** is the same (The Context).
-   The **Game Cartridge** you plug in is the "Strategy."
-   If you want to play a racing game, you plug in the Racing Strategy. If you want a fighting game, you swap the cartridge. The console doesn't care what game it is; it just knows how to run "Cartridges."

---

## 🏗️ The "Messy" Way (Anti-Pattern)

Avoid code like this, which grows forever and is hard to test:

```javascript
function checkout(amount, method) {
  if (method === 'stripe') {
    // 50 lines of Stripe logic
  } else if (method === 'paypal') {
    // 50 lines of PayPal logic
  } else if (method === 'crypto') {
    // 50 lines of Crypto logic
  }
}
```

---

## 🏗️ The Strategy Way (Clean)

We define different "Strategies" and just tell the processor which one to use.

```javascript
// 1. Define the Strategies
const stripeStrategy = (amount) => console.log(`Charging $${amount} via Stripe...`);
const paypalStrategy = (amount) => console.log(`Charging $${amount} via PayPal...`);
const cryptoStrategy = (amount) => console.log(`Charging $${amount} via Bitcoin...`);

// 2. The Context (The Console)
class PaymentProcessor {
  constructor() {
    this.strategy = null;
  }

  setStrategy(strategy) {
    this.strategy = strategy;
  }

  process(amount) {
    return this.strategy(amount);
  }
}

// 3. Usage
const checkout = new PaymentProcessor();

checkout.setStrategy(stripeStrategy);
checkout.process(100);

checkout.setStrategy(cryptoStrategy);
checkout.process(100);
```

---

## 🚀 Why Use the Strategy Pattern?

1.  **Open/Closed Principle:** You can add a new payment method (like "Apple Pay") by just writing a new function, without touching the `PaymentProcessor` code.
2.  **Testability:** You can test each strategy function individually.
3.  **Readability:** It turns a 500-line function into several small, 20-line functions.

---

## 📐 Visualizing the Strategy Swap

```text
    [ PAYMENT PROCESSOR ] ◀─────── (Plug-in) ─────── [ STRATEGY ]
             │                                          │
             ▼                                          ▼
    [ Runs process() ] ◀─────────────────────── [ Runs logic() ]
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### Polymorphism & Inline Caches
In V8, if you call the same function name on different objects (Polymorphism), V8 tries to optimize it using **Inline Caches (IC)**. If your "Strategies" all have the same structure (e.g., they are all functions that take one argument), V8 can remember where the machine code for that logic is stored, making the "swap" almost as fast as a regular function call.

---

## 💼 Interview Questions

**Q1: How does Strategy Pattern differ from a simple `switch` statement?**
> **Ans:** A `switch` statement is "hard-coded." To add a new case, you must modify the function. In the Strategy pattern, you can add new behaviors at any time from anywhere in your app without touching the original code.

**Q2: Can you use the Strategy Pattern for form validation?**
> **Ans:** Yes! It’s perfect for it. You can have an `EmailStrategy`, `MinLengthStrategy`, and `RequiredStrategy`, and then just pass a list of these strategies to your validation engine.

**Q3: Is the Strategy Pattern only for Classes?**
> **Ans:** No. In JavaScript, since functions are "first-class objects," you can just use a plain object of functions as your strategies. This is often called the "Strategy Object" pattern.

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **Strategy Pattern** | Clean and highly scalable. | Requires more files/functions up front. |
| **Switch Statement** | Very fast to write for simple logic. | Becomes a "Maintenance Nightmare" as it grows. |
| **Inheritance** | Shared code between types. | "Fragile Base Class" problem; very rigid. |

---

## 🔗 Navigation

**Prev:** [04_Observer_Pattern.md](04_Observer_Pattern.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [06_Middleware_Pattern.md](06_Middleware_Pattern.md)
