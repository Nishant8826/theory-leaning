# Signals

## What is it?
Angular Signal ek value ke charo taraf ek reactive wrapper container hota hai jo apne consumers (jahan wo read ho raha hai) ko value update hone par alert notify karta. Signals Angular application me high-performance, fine-grained reactivity lane ka kaam karte hain, jisse framework ko exact pata chalta hai ki state variable kahan read hua hai aur kis browser HTML template node ko update karna hai.

## Why do we need it?
Legacy Angular versions me, change updates check karne ke liye Zone.js engine pure component tree ko check/verify (dirty checking) karta tha jab bhi koi asynchronous click, timer, ya HTTP request handle hoti thi. Yeh approach bade applications me slow rendering performance generate karta tha. Signals change checking process ko exact specific element level par target karta hai, jisse dynamic rendering bina Zone.js engine background overheads ke run ho sakti hai (Zoneless applications).

```
Zone.js Change Detection (Coarse-Grained):
Async Event ──> Zone.js intercepts ──> Check entire component tree ──> Re-render modified elements

Signals Change Detection (Fine-Grained):
Signal value updates ──> Notify only elements bound to Signal ──> Re-render specific DOM nodes
```

## How does it work?
1. **Writable Signals (`signal()`)**: Aise mutable state wrappers jinhe direct `.set(newValue)` ya `.update(val => nextVal)` methods se change kiya ja sakta hai.
2. **Computed Signals (`computed()`)**: Aise read-only reactive signals jo doosre dependent signals se values calculate karte hain. Yeh lazy values compute karte hain aur inputs references updates hone tak values cached memory me hold karte hain.
3. **Effects (`effect()`)**: Developer hooks logic jo read coordinate signals change hone par background actions (jaise logging, storage save) trigger karte hain.
4. **Signal Inputs (`input()`)**: Modern, high-performance signals inputs attributes jo legacy decorator style `@Input()` wrapper settings ko replace karte hain.

## Impact
* **Application Architecture**: Direct component state tracking ko simple aur boiler-plate free banata hai.
* **Performance**: Browser DOM change detection processing time drastically reduce karta hai, jisse modern Zoneless application initialization clean execute hoti hai.
* **Maintainability**: Data dependencies flow logic fully visible rakhta hai, kyunki dependencies update hone par computed models automatically recalculate ho jate hain.

## Real World Example
E-commerce payment bill settings screen me, signals dynamic checkout inputs (item quantity, tax rate, discount coupons) monitor karte hain. Jaise hi quantity counter increment hota, billing subtotal `computed()` automatically values recalculate kar deta hai.

## Syntax
* **Declare a Writable Signal**: `const count = signal(0);`
* **Read a Signal**: `count()`
* **Set a Value**: `count.set(5);`
* **Update based on current value**: `count.update(val => val + 1);`
* **Declare Computed Signal**: `const double = computed(() => count() * 2);`
* **Signal Input**: `name = input<string>('guest');`

## Code Examples
Neeche Writable Signals, Computed Signals, Effects, aur Signal Inputs ka dynamic cart component example diya gaya hai:

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
1. **Always Use Computed for Derived State**: Derived values computations calculate karne ke liye custom effect write loops avoid karein. Humesha `computed()` wrappers ka use karein.
2. **Limit Side Effects in Effects**: `effect()` hooks block ke andar writable signals values state modify (`.set()`, `.update()`) karna avoid karein jag tak setup `allowSignalWrites` override configuration explicitly set na ho, nahi toh infinite loops create ho sakte hain.
3. **Pipes and Signals**: HTML templates variables me dynamic filters pipelines apply karte waqt signals execution syntax parameters function key `()` lagana na bhoolein: `{{ price() | currency }}`.

## Common Mistakes
* **Forgetting to Call the Signal**: Template UI ya TS code lines parsing me signals parameters brackets references missing hona, jaise query line me `{{ quantity }}` likhna `{{ quantity() }}` ke bajaye. Isse output print values text ke bajaye internal JS function signature show karta hai.
* **Overusing RxJS for Local State**: Components basic local status indicators (jaise menu show/hide checks) manage karne ke liye complex RxJS `BehaviorSubject` streams deploy karna. In basic tasks ke liye writable signals simple aur neat option hain.

## Interview Questions & Answers
### Q: What are the main differences between Signals and RxJS Observables?
**A**: Signals UI status details maintain karne ke liye design huye hain jinme hamesha synchronous default value exist karti hai. Observables async event pipelines ke liye bane hain jo complex data modifiers (jaise debounce, filtering) execute kar sakte hain.

### Q: Why are computed signals performant?
**A**: Computed signals lazy assessment aur cache memory calculations use karte hain. Yeh tab tak computations compute nahi karte jab tak logic call na ho, aur dependencies updates hone par hi calculations refresh karte hain.

## Summary
Signals Angular applications me fine-grained reactivity add karte hain. Writable signals variables holds state, computed signals derived memory cache calculations aur effects background side-effects execute karte hain. Signals implementation local state tracking simple banata hai aur Zoneless rendering enable karta hai.

---

Previous : [Component Communication](./09_Component_Communication.md) | Index : [Home](./00_index.md) | Next : [Dependency Injection](./11_Dependency_Injection.md)
