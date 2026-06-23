# Enterprise Architecture

## What is it?
Enterprise Architecture ek system design framework hai jise large-scale Angular applications ko structure karne ke liye use kiya jata hai. Yeh define karta hai ki folder structures, domain boundaries, feature modules, aur application layers (jaise UI, State, aur Data layers) ko kaise organize kiya jaye taaki codebase ko multiple development teams ke beech maintainable rakha ja sake.

## Why do we need it?
Bina ek structured architecture ke, large codebases me features badhne ke sath hi unhe maintain karna bohot difficult ho jata hai. Developers redundant API integrations likh sakte hain, business logic ko presentation code ke sath mix kar sakte hain, ya tightly coupled components bana sakte hain. Structured architectural boundaries (jaise Domain-Driven Design aur Smart/Dumb component separation) enforce karne se codebases clean aur scalable rehte hain.

```
Enterprise Layered Architecture:
┌────────────────────────────────────────────────────────┐
│                        UI Layer                        │
│             (Dumb Components / Presentational)         │
│└──────────────────────────┬─────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│                        State Layer                     │
│             (NgRx Store / Signals State / Smart)       │
│└──────────────────────────┬─────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│                        Data Layer                      │
│             (API Services / Http Clients)              │
└────────────────────────────────────────────────────────┘
```

## How does it work?
1. **Domain-Driven Design (DDD)**: Yeh applications ko isolated domain folders (jaise `billing`, `catalog`, `shipping`) me divide karta hai. Har domain ka apna khud ka features, state, aur UI hota hai.
2. **Smart Components (Container)**: Yeh state ko manage karte hain, services ya store actions ko subscribe karte hain, aur core routing events ko handle karte hain.
3. **Dumb Components (Presentational)**: Yeh inputs ke zariye data receive karte hain, outputs ke zariye user interactions trigger karte hain, aur inka services ya APIs par koi direct dependency nahi hoti.
4. **Layered Boundaries**:
   - **Core Layer**: Singletons jo application bootstrap ke dauran instantiate hote hain (jaise authentication configurations aur guards).
   - **Shared Layer**: Reusable components, directives, aur pipes (jaise custom buttons, loading spinners, aur layout grids) jinhe kahin bhi import kiya ja sakta hai.
   - **Feature Layer**: Kisi particular feature ke specific components aur business logic ko contain karta hai.

## Impact
* **Application Architecture**: Tight coupling ko rokta hai, jisse features ko locate, test, aur refactor karna easy ho jata.
* **Performance**: Modular, domain-driven boundaries feature files ko lazy-load karna simple bana deti hain.
* **Scalability**: Multiple developers bina merge conflicts ke parallelly alag-alag domains par kaam kar sakte hain.

## Real World Example
Ek multi-team retail portal me, customer service domain aur checkout payment domain ko alag-alag folders me structure kiya jata hai. Checkout team customer service features ko impact kiye bina ya use rebuild kiye bina payment methods aur gateways ko update kar sakti hai.

## Syntax
Angular workspace ke liye ek enterprise-grade folder structure:
```
src/
├── app/
│   ├── core/              # Singletons (Auth, Guards, Interceptors)
│   ├── shared/            # Reusable UI elements (Buttons, Spinners)
│   └── domains/           # Domain folders
│       ├── billing/       # Billing Domain
│       │   ├── data/      # API services, models
│       │   ├── state/     # NgRx / Signal stores
│       │   └── features/  # Smart / Dumb components
│       └── catalog/       # Catalog Domain
```

## Code Examples
Neeche **Smart and Dumb Component** pattern ka implementation diya gaya hai.

### `product-card.component.ts` (Dumb Component: Presentational)
```typescript
import { Component, Input, Output, EventEmitter, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface ProductItem {
  id: string;
  title: string;
  price: number;
}

@Component({
  selector: 'app-product-card',
  standalone: true,
  imports: [CommonModule],
  changeDetection: ChangeDetectionStrategy.OnPush, // High performance
  template: `
    <div class="card">
      <h4>{{ product.title }}</h4>
      <p>Price: {{ product.price | currency }}</p>
      
      <!-- Emit events up to parent container -->
      <button (click)="select.emit(product)">Quick View</button>
    </div>
  `,
  styles: [`
    .card { border: 1px solid #d1d5db; padding: 16px; border-radius: 6px; }
  `]
})
export class ProductCardComponent {
  // Receives immutable data from parent container
  @Input({ required: true }) product!: ProductItem;
  
  // Emits user interaction events up to parent container
  @Output() select = new EventEmitter<ProductItem>();
}
```

### `product-catalog.component.ts` (Smart Component: Container)
```typescript
import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProductCardComponent, ProductItem } from './product-card.component';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-product-catalog',
  standalone: true,
  imports: [CommonModule, ProductCardComponent],
  template: `
    <div class="catalog-container">
      <h3>Store Catalog (Smart Container)</h3>
      
      <div class="grid">
        <!-- Dumb components handle presentation -->
        <app-product-card 
          *ngFor="let item of products()" 
          [product]="item" 
          (select)="handleProductSelect($event)">
        </app-product-card>
      </div>

      <div *ngIf="selectedProduct()" class="modal">
        <p>Selected Product: {{ selectedProduct()?.title }}</p>
      </div>
    </div>
  `,
  styles: [`
    .catalog-container { padding: 20px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; }
    .modal { margin-top: 20px; background: #f3f4f6; padding: 15px; border-radius: 6px; }
  `]
})
export class ProductCatalogComponent implements OnInit {
  private http = inject(HttpClient);

  // Manage state and data logic
  products = signal<ProductItem[]>([]);
  selectedProduct = signal<ProductItem | null>(null);

  ngOnInit() {
    this.http.get<ProductItem[]>('https://api.my-app.com/products')
      .subscribe(data => this.products.set(data));
  }

  handleProductSelect(product: ProductItem) {
    this.selectedProduct.set(product);
  }
}
```

## Best Practices
1. **Enforce Smart/Dumb Separation**: Presentational components ko services, APIs, ya state se clean rakhein. Data aur events pass karne ke liye inputs aur outputs ka use karein.
2. **Organize by Domain**: Related components, services, aur state ko domain wise group karein, jisse features ko manage aur navigate karna easy ho.
3. **Use Lint rules (Nx boundary tags)**: Monorepos use karte waqt lint rules configure karein taaki ek domain dusre domain ke private files ko import na kar sake.

## Common Mistakes
* **Injecting Services into Dumb Components**: Presentational components me directly services inject karna. Isse unhe test karna aur in isolation reuse karna mushkil ho jata hai.
* **Bloated Shared Layer**: Feature-specific components ko global shared folder me rakhna. Shared directories me sirf generic, reusable UI controls (jaise buttons, inputs, aur spinners) hi hone chahiye.

## Interview Questions & Answers
### Q: What is the difference between a Smart Component and a Dumb Component?
**A**: Smart Components (jaise page containers) app ke logical brain hote hain—yeh API calls handle karte hain, service inject karte hain, routes handle karte hain aur state manage karte hain. Dumb Components (presentational components) sirf UI dikhane ke liye hote hain—yeh bina kisi service ko inject kiye, data parent component se `@Input()` dwara lete hain aur user events `@Output()` dwara parent ko pass kar dete hain, jisse inhen pure project me kahin bhi reuse kiya ja sake.

### Q: Why do we separate applications by domain folders?
**A**: Domain folders (jaise checkout, auth, billing) me application ko divide karne se tight coupling (ek feature ka dusre feature par dependent hona) khatam hoti hai. Isse code easily manage hota, lazy-loading setup karna simple ho jata hai, aur different teams bina ek dusre ke code ko impact kiye parallelly alag feature modules par kaam kar sakti hain.

## Summary
Enterprise Angular architectures me codebase ko scalable rakhne ke liye Domain-Driven Design (DDD) ka use hota. Presentation (Dumb components) ko logic (Smart components) se separate rakhna aur files ko domain wise organize karna maintainable applications banane me help karta hai.

---

Previous : [SSR and Advanced Concepts](./24_SSR_and_Advanced_Concepts.md) | Index : [Home](./00_index.md) | Next : [Deployment and CI/CD](./26_Deployment_and_CI_CD.md)
