# Signals

## What is it?
An Angular Signal is a reactive wrapper around a value that notifies consumers whenever that value changes. Signals introduce fine-grained reactivity to Angular, allowing the framework to know exactly where state is read and precisely which DOM elements require updating.

## Why do we need it?
Historically, Angular has relied on Zone.js to check the entire component tree for updates on every async event (like clicks, timers, or HTTP responses). This "dirty checking" approach is inefficient, as parts of the DOM that didn't change are still scanned. Signals enable fine-grained updates, allowing components to run without Zone.js (Zoneless applications).

```
Zone.js Change Detection (Coarse-Grained):
Async Event ──> Zone.js intercepts ──> Check entire component tree ──> Re-render modified elements

Signals Change Detection (Fine-Grained):
Signal value updates ──> Notify only elements bound to Signal ──> Re-render specific DOM nodes
```

## How does it work?
1. **Writable Signals (`signal()`)**: Holds state that can be directly updated using `.set()` or `.update()`.
2. **Computed Signals (`computed()`)**: Read-only reactive values derived from other signals. They are lazily evaluated and cache their values until their dependencies change.
3. **Effects (`effect()`)**: Developer hooks that execute side-effect logic whenever the signals read inside them change.
4. **Signal Inputs (`input()`)**: A modern, signal-based alternative to the legacy `@Input()` decorator.

## Impact
* **Application Architecture**: Simplifies local state tracking, reducing boilerplate compared to RxJS streams for basic UI states.
* **Performance**: Drastically reduces change detection overhead, paving the way for Zoneless rendering.
* **Maintainability**: Makes data dependencies clear, as computed signals update automatically based on their dependencies.

## Real World Example
In a shopping cart checkout form, signals track quantity, price, discount codes, and taxes. As quantity scales up or down, the total price (computed) recalculates instantly without manual event listeners.

## Syntax
* **Declare a Writable Signal**: `const count = signal(0);`
* **Read a Signal**: `count()`
* **Set a Value**: `count.set(5);`
* **Update based on current value**: `count.update(val => val + 1);`
* **Declare Computed Signal**: `const double = computed(() => count() * 2);`
* **Signal Input**: `name = input<string>('guest');`

## Hinglish Explanation

Agar aap Angular me state management aur Change Detection ko simple aur super-fast banana chahte hain, toh **Signals** ko samajhna zaroori hai.

### 1. Signals Kya Hain? (Signal is a Container)
Normal JavaScript variables me value change hoti hai, toh Angular ko khud se nahi pata chalta ki use page (UI) par kahan update karna hai.
**Signal** ek reactive container (wrapper) hai jo kisi value ko hold karta hai. Jab bhi iski value change hoti hai, toh yeh Angular ko notify karta hai: 
*"Bhai! Meri value change ho gayi hai, jahan-jahan main use ho raha hoon, wahan screen ko update kar do!"*

### 2. Zone.js vs Signals (Purana vs Naya tareeka)
* **Zone.js (Dirty Checking - Old Way):** Pehle jab bhi koi event (jaise click, timer, ya API response) hota tha, toh Zone.js pure component tree ko upar se neeche tak check karta tha ki kahin kuch change toh nahi hua. Yeh bilkul waisa hai jaise pure building me check karna ki kis room ka fan band hai.
* **Signals (Fine-grained - New Way):** Signals ke aane se Angular ko exact pata hota hai ki kaunsi value kis component me kis HTML tag par use ho rahi hai. Value change hone par Angular **sirf usi specific HTML element ko update** karta hai. Baaki components ko chhua tak nahi jata! Isse performance bohot badh jati hai.

### 3. Signals Ke Teen Main Pillars (Core Features)

#### A. Writable Signals (`signal()`)
Yeh ek simple box ki tarah hai jisme value store hoti hai aur hum jab chahein use change kar sakte hain.
* **Read Kaise Karein?** Signal ko padhne ke liye function ki tarah execute karna padta hai: `mySignal()`.
* **Value Update Kaise Karein?**
  * Direct change karne ke liye: `count.set(5)`
  * Purani value par depend karke change karne ke liye: `count.update(val => val + 1)`

#### B. Computed Signals (`computed()`)
Yeh read-only signals hote hain jo kisi dusre signal ke badalne par **automatically recalculate** ho jate hain.
* **Example:** `total = computed(() => qty() * price())`
* **Fayde:** 
  1. **Lazy Evaluation:** Yeh tab tak calculate nahi hote jab tak inki value ko kahin read na kiya jaye.
  2. **Caching:** Agar dependents (`qty` ya `price`) ki value change nahi hui, toh yeh calculation dobara nahi karte, purani cached value hi return kar dete hain.

#### C. Effects (`effect()`)
Jab bhi koi signal change ho aur aapko koi external kaam (side-effect) karna ho, tab `effect()` ka use hota hai.
* **Example:** Jab bhi counter badle, local storage me value save karna:
  ```typescript
  effect(() => {
    localStorage.setItem('counter', this.count().toString());
  });
  ```
* **Note:** Iska use main UI business logic ke liye nahi, balki logging, analytics, local storage update, ya custom DOM integration ke liye kiya jata hai.

### 4. Real-World Analogy (Ghar aur Light Bulbs)
Socho ki aapke ghar me 10 rooms hain.
* **Old Way (Zone.js):** Ek room ka switch daba, toh poore ghar ke har ek room ke bulb ko check kiya gaya ki wo sahi chal raha hai ya nahi. (Slow & unnecessary).
* **New Way (Signals):** Har bulb ko pata hai ki uska switch kaunsa hai. Jaise hi switch (Signal) daba, sirf wahi specific bulb (DOM Element) notify hua aur turn on/off ho gaya. (Super Fast & Clean).

## Code Examples
Below is a complete implementation demonstrating Writable Signals, Computed Signals, Effects, and Signal Inputs.

### `cart-calculator.component.ts`
```typescript
import { Component, signal, computed, effect, input } from '@angular/core';

@Component({
  selector: 'app-cart-calculator',
  standalone: true,
  template: `
    <div class="cart-box">
      <h4>Order Invoice for {{ customerName() }}</h4>

      <div class="price-row">
        <label>Unit Price: $120.00</label>
      </div>

      <div class="control-row">
        <button (click)="decrement()">-</button>
        <span class="qty">Quantity: {{ quantity() }}</span>
        <button (click)="increment()">+</button>
      </div>

      <hr />

      <div class="totals">
        <p>Subtotal: {{ subtotal() | currency }}</p>
        <p>Tax (15%): {{ tax() | currency }}</p>
        <p class="grand-total">Grand Total: {{ grandTotal() | currency }}</p>
      </div>
    </div>
  `,
  styles: [`
    .cart-box { border: 2px solid #8b5cf6; padding: 20px; border-radius: 8px; max-width: 320px; }
    .qty { margin: 0 12px; font-weight: bold; }
    .grand-total { font-weight: bold; color: #7c3aed; font-size: 18px; }
  `]
})
export class CartCalculatorComponent {
  // 1. Signal Input (declared inside component)
  customerName = input<string>('Guest User');

  // 2. Writable Signal
  quantity = signal<number>(1);

  // 3. Computed Signals (read-only and cached)
  subtotal = computed(() => this.quantity() * 120.00);
  tax = computed(() => this.subtotal() * 0.15);
  grandTotal = computed(() => this.subtotal() + this.tax());

  constructor() {
    // 4. Effect hook (runs whenever read signals change)
    effect(() => {
      console.log(`Cart updated. New Grand Total: $${this.grandTotal()}`);
    });
  }

  increment(): void {
    this.quantity.update(q => q + 1);
  }

  decrement(): void {
    if (this.quantity() > 1) {
      this.quantity.update(q => q - 1);
    }
  }
}
```

## Best Practices
1. **Always Use Computed for Derived State**: Do not manually update a writable signal inside an effect to store derived calculations. Use `computed()` instead.
2. **Limit Side Effects in Effects**: Avoid setting other writable signals inside an `effect()` unless explicitly configured (`allowSignalWrites: true`), as this can lead to infinite update loops.
3. **Pipes and Signals**: When binding a signal in a template, invoke it as a function before applying pipes: `{{ price() | currency }}`.

## Common Mistakes
* **Forgetting to Call the Signal**: Forgetting the parenthesis when reading a signal in a template or logic block, e.g. writing `{{ quantity }}` instead of `{{ quantity() }}`. This binds the signal function reference itself instead of its value.
* **Overusing RxJS for Local State**: Converting simple boolean toggles (like menu open/closed states) into RxJS BehaviorSubjects. Use writable signals instead to reduce boilerplate.

## Interview Questions & Answers
### Q: What are the main differences between Signals and RxJS Observables?
**A**: Signals are designed for state management; they always hold an active value, are read synchronously, and are optimized for UI data-binding. Observables are designed for event streams; they deliver values asynchronously over time, support complex transformations (filtering, debouncing), and do not need to hold a default starting value.
* **Hinglish Explanation**: Signals ko primary UI state track karne ke liye design kiya gaya hai; inme hamesha ek core active value rehti hai jo synchronously bina kisi subscription ke read ki ja sakti hai. Dusri taraf, RxJS Observables event streams aur data pipelines ke liye hain; yeh asynchronously multiple events deliver kar sakte hain, inme custom operations (debounce, mapping) support hote hain, aur inme default value hona compulsory nahi hai.

### Q: Why are computed signals performant?
**A**: Computed signals are lazily evaluated and cache their values. They only run their calculations when read, and only recalculate if one of the signals they depend on emits a new value, preventing unnecessary work during change detection.
* **Hinglish Explanation**: Computed signals performance ke mamle me bohot smart hote hain kyunki yeh lazy evaluation aur caching concept par kaam karte hain. Jab tak inki value ko HTML ya code me call na kiya jaye, yeh calculation nahi karte. Aur agar dependent signals ki value nahi badli hai, toh yeh purani cached value hi return karte hain bina calculations ko repeat kiye.

## Summary
Signals introduce fine-grained reactivity to Angular. Writable signals hold state, computed signals derive cached values, and effects run side effects. Using signals simplifies local state tracking and enables Zoneless change detection.

---

Previous : [Component Communication](./09_Component_Communication.md) | Index : [Home](./00_index.md) | Next : [Dependency Injection](./11_Dependency_Injection.md)
