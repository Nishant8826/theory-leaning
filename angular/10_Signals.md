# Signals

## What is it?
An Angular Signal is a reactive wrapper around a value that automatically notifies interested consumers (templates, computed values, or effects) whenever that value changes. Signals introduce fine-grained reactivity to Angular, allowing the framework to know precisely where a state variable is read and update only the specific DOM nodes that depend on it.

## Why do we need it?
In previous versions of Angular, change detection relied entirely on Zone.js to intercept asynchronous browser events (clicks, timers, HTTP responses) and check the entire component tree from top to bottom (dirty checking). On large, complex applications, this top-down checking can cause UI frame drops and performance bottlenecks. 

Signals solve this problem by introducing fine-grained dependency tracking. The framework updates only the specific DOM nodes bound to a changed Signal, paving the way for high-performance, Zoneless Angular applications.

```
Zone.js Change Detection (Coarse-Grained):
Async Event ──> Zone.js intercepts ──> Check entire component tree ──> Re-render modified elements

Signals Change Detection (Fine-Grained):
Signal value updates ──> Notify only elements bound to Signal ──> Re-render specific DOM nodes
```

## How does it work?
1. **Writable Signals (`signal()`)**: Mutable state containers whose values can be modified directly using `.set(newValue)` or `.update(val => nextVal)`.
2. **Computed Signals (`computed()`)**: Read-only reactive values derived from other signals. They are computed lazily and memoize (cache) their return value until their underlying signal dependencies change.
3. **Effects (`effect()`)**: Reactive callback functions that automatically re-run whenever any of the signals read inside them emit a new value. Used for side effects such as logging, analytics, or manual DOM/storage synchronization.
4. **Signal Inputs (`input()`)**: The modern, signal-based replacement for the traditional `@Input()` decorator, providing clean reactivity and type safety.

## Impact
* **Application Architecture**: Simplifies local component state management by eliminating boilerplate Subject/Observable streams for synchronous state.
* **Performance**: Drastically reduces change detection computation time and unlocks fully Zoneless Angular applications (`provideExperimentalZonelessChangeDetection()`).
* **Maintainability**: Makes data dependency graphs clear and declarative; derived state updates automatically and predictably.

## Real World Example
In an e-commerce checkout screen, Writable Signals track dynamic user inputs (item quantity, promo code, shipping method). As the quantity changes, `computed()` signals automatically recalculate the subtotal, sales tax, shipping fee, and grand total without manual event wiring.

## Syntax
* **Declare a Writable Signal**: `const count = signal(0);`
* **Read a Signal**: `count()`
* **Set a Value**: `count.set(5);`
* **Update based on previous value**: `count.update(val => val + 1);`
* **Declare a Computed Signal**: `const double = computed(() => count() * 2);`
* **Declare a Signal Input**: `customerName = input<string>('Guest');`

## Code Examples
Below is a complete shopping cart invoice component demonstrating Writable Signals, Computed Signals, Effects, and Signal Inputs:

```typescript
import { Component, signal, computed, effect, input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-cart-calculator',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="cart-box">
      <h4>Order Invoice for: {{ customerName() }}</h4>

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
    .cart-box { 
      border: 2px solid #8b5cf6; 
      padding: 20px; 
      border-radius: 8px; 
      max-width: 340px; 
      font-family: sans-serif;
    }
    .qty { 
      margin: 0 14px; 
      font-weight: bold; 
    }
    .control-row {
      margin: 15px 0;
    }
    .control-row button {
      padding: 4px 12px;
      font-size: 16px;
      cursor: pointer;
    }
    .grand-total { 
      font-weight: bold; 
      color: #7c3aed; 
      font-size: 18px; 
    }
  `]
})
export class CartCalculatorComponent {
  // 1. Signal Input
  customerName = input<string>('Guest User');

  // 2. Writable Signal
  quantity = signal<number>(1);

  // 3. Computed Signals (lazily evaluated and cached)
  subtotal = computed(() => this.quantity() * 120.00);
  tax = computed(() => this.subtotal() * 0.15);
  grandTotal = computed(() => this.subtotal() + this.tax());

  constructor() {
    // 4. Effect hook (automatically tracks grandTotal signal reads)
    effect(() => {
      console.log(`[Analytics] Order updated. New Grand Total: $${this.grandTotal()}`);
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
1. **Always Use `computed()` for Derived State**: Avoid writing manual update functions or triggering effects to recalculate derived values. `computed()` ensures optimal memoization and prevents redundant recalculations.
2. **Avoid Modifying State Inside Effects**: Do not call `.set()` or `.update()` inside an `effect()` callback unless `allowSignalWrites: true` is explicitly configured. Modifying state inside effects can cause cyclical triggers and infinite loops.
3. **Always Invoke the Signal in Templates**: Remember to include parentheses `()` when reading signals in HTML templates (e.g., `{{ quantity() }}` instead of `{{ quantity }}`).

## Common Mistakes
* **Forgetting Parentheses `()` When Reading**: Referencing a signal as `{{ quantity }}` in the template renders the underlying JavaScript function definition rather than the evaluated value. Always invoke it as `{{ quantity() }}`.
* **Using RxJS for Simple Local State**: Using complex `BehaviorSubject` streams with manual unsubscriptions for basic local variables (like modal visibility or a toggle flag). Writable signals are far simpler and cleaner for synchronous local state.

## Interview Questions & Answers
### Q: What is the primary difference between Angular Signals and RxJS Observables?
**A**: Signals are designed for synchronous state management; they always hold a current value, provide synchronous reading via getter invocation `signal()`, and offer fine-grained UI dependency tracking. RxJS Observables represent asynchronous event streams over time, excelling at complex asynchronous pipelines involving operators like `debounceTime`, `switchMap`, and `catchError`.

### Q: Why are Computed Signals so performant?
**A**: Computed signals are evaluated lazily and leverage memoization. They only recompute when their value is actually read by a consumer, and they only recalculate when at least one of their recorded signal dependencies emits a new value.

## Summary
Signals introduce fine-grained, high-performance reactivity to Angular. Writable signals manage mutable state, computed signals provide cached derived calculations, and effects handle reactive side effects. Signals simplify state tracking and serve as the foundation for modern Zoneless Angular applications.

---

Previous : [Component Communication](./09_Component_Communication.md) | Index : [Home](./00_index.md) | Next : [Dependency Injection](./11_Dependency_Injection.md)
