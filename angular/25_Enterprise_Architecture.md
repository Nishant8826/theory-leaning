# Enterprise Architecture

## What is it?
Enterprise Architecture is the system design framework used to structure large-scale Angular applications. It defines how folder structures, domain boundaries, feature modules, and application layers (such as UI, State, and Data layers) are organized to keep the codebase maintainable across multiple development teams.

## Why do we need it?
Without a structured architecture, large codebases can become difficult to maintain as features grow. Developers may write redundant API integrations, mix business logic with presentation code, or create tightly coupled components. Enforcing structured architectural boundaries (like Domain-Driven Design and Smart/Dumb component separation) keeps codebases clean and scalable.

```
Enterprise Layered Architecture:
┌────────────────────────────────────────────────────────┐
│                        UI Layer                        │
│             (Dumb Components / Presentational)         │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│                        State Layer                     │
│             (NgRx Store / Signals State / Smart)       │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│                        Data Layer                      │
│             (API Services / Http Clients)              │
└────────────────────────────────────────────────────────┘
```

## How does it work?
1. **Domain-Driven Design (DDD)**: Partitions applications into isolated domain folders (e.g. `billing`, `catalog`, `shipping`). Each domain contains its own features, state, and UI.
2. **Smart Components (Container)**: Manage state, subscribe to services or store actions, and handle core routing events.
3. **Dumb Components (Presentational)**: Receive data via inputs, trigger user interactions via outputs, and contain no direct dependencies on services or APIs.
4. **Layered Boundaries**:
   - **Core Layer**: Singletons instantiated during application bootstrap (such as authentication configurations and guards).
   - **Shared Layer**: Reusable components, directives, and pipes (such as custom buttons, loading spinners, and layout grids) that can be imported anywhere.
   - **Feature Layer**: Contains components and business logic specific to individual features.

## Impact
* **Application Architecture**: Prevents tight coupling, making features easy to locate, test, and refactor.
* **Performance**: Modular, domain-driven boundaries make features easy to lazy-load.
* **Scalability**: Multiple developers can work on separate domains concurrently without merge conflicts.

## Real World Example
In a multi-team retail portal, the customer service domain and the checkout payment domain are structured in separate folders. The checkout team updates payment methods and gateways without affecting or rebuilding the customer service features.

## Syntax
An enterprise-grade folder structure for an Angular workspace:
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

## Hinglish Explanation

Enterprise-level Angular applications ko handle karne ke liye clean structural code design ke do core rules hain:

### 1. Smart vs Dumb Components Pattern (Dimaag vs Display)
* **Smart Components:** Inhe containers bhi bolte hain. Inka kaam data logical services handle karna, routes parameters dynamic check karna, aur API calls trigger karna hota hai.
* **Dumb Components:** Inka kaam sirf visual render (display UI layout) karna hota hai. Inka koi connection network requests ya state services se nahi hota. Yeh strictly inputs ke through data receive karte hain aur outputs se events emit karte hain. Isse inka test execution aur reusability bohot strong ho jati hai.

### 2. Domain-Driven Design (Feature division)
* Code folder grouping business features ke base par honi chahiye (jaise checkout module, payment features, account profile).
* **Shared Folder Restrictions:** Shared layer ke andar feature-specific business details nahi honi chahiye, wahan sirf universal global helpers (jaise custom loading spinner, common format custom pipes, basic custom wrapper button layouts) hone chahiye.

## Code Examples
Below is an implementation of the **Smart and Dumb Component** pattern.

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
1. **Enforce Smart/Dumb Separation**: Keep presentational components clean of services, APIs, or state. Use inputs and outputs to pass data and events.
2. **Organize by Domain**: Group related components, services, and state by domain, making features easy to manage and navigate.
3. **Use Lint rules (Nx boundary tags)**: When using Monorepos, configure lint rules to prevent domains from importing private files from other domains.

## Common Mistakes
* **Injecting Services into Dumb Components**: Injecting services directly into presentational components. This makes them difficult to reuse or test in isolation.
* **Bloated Shared Layer**: Placing feature-specific components inside the global shared folder. Shared directories should only contain generic, reusable UI controls (such as buttons, inputs, and spinners).

## Interview Questions & Answers
### Q: What is the difference between a Smart Component and a Dumb Component?
**A**: Smart components (containers) manage state, interact with services, handle routing, and dispatch actions. Dumb components (presentational) focus on rendering UI layouts. They receive data through inputs and emit interactions through outputs, keeping them reusable and easy to test.
* **Hinglish Explanation**: Smart Components (jaise page containers) app ke logical brain hote hain—yeh API calls handle karte hain, service inject karte hain, routes handle karte hain aur state manage karte hain. Dumb Components (presentational components) sirf UI dikhane ke liye hote hain—yeh bina kisi service ko inject kiye, data parent component se `@Input()` dwara lete hain aur user events `@Output()` dwara parent ko pass kar dete hain, jisse inhen pure project me kahin bhi reuse kiya ja sake.

### Q: Why do we separate applications by domain folders?
**A**: Separating applications by domain folders groups related features together, making codebases easier to maintain. This approach prevents tight coupling, makes lazy-loading straightforward, and allows multiple teams to work on separate domains concurrently.
* **Hinglish Explanation**: Domain folders (jaise checkout, auth, billing) me application ko divide karne se tight coupling (ek feature ka dusre feature par dependent hona) khatam hoti hai. Isse code easily manage hota hai, lazy-loading setup karna simple ho jata hai, aur different teams bina ek dusre ke code ko impact kiye parallelly alag feature modules par kaam kar sakti hain.

## Summary
Enterprise Angular architectures use Domain-Driven Design (DDD) to keep codebases scalable. Separating presentation (Dumb components) from logic (Smart components) and organizing files by domain helps build maintainable applications.

---

Previous : [SSR and Advanced Concepts](./24_SSR_and_Advanced_Concepts.md) | Index : [Home](./00_index.md) | Next : [Deployment and CI/CD](./26_Deployment_and_CI_CD.md)
