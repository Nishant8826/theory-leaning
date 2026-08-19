# Enterprise Architecture

## What is it?
Enterprise Architecture is the system design methodology used to structure, organize, and scale large enterprise Angular applications. It defines standards for folder structures, domain boundaries, state layer segregation, and code sharing across multiple autonomous engineering teams.

## Why do we need it?
Without a disciplined architectural framework, large enterprise codebases degrade into chaotic, monolithic structures as features grow. Developers create tight coupling between unrelated views, mix presentation code with API calls, and build duplicate services. 

Enforcing clear architectural boundaries—such as Domain-Driven Design (DDD) and the Container/Presentational (Smart/Dumb) component pattern—ensures codebases remain modular, scalable, testable, and maintainable over years of continuous development.

```
Enterprise Layered Architecture:
┌────────────────────────────────────────────────────────┐
│                        UI Layer                        │
│             (Dumb / Presentational Components)         │
└──────────────────────────┬─────────────────────────────┘
                           │ Inputs (Data) / Outputs (Events)
                           ▼
┌────────────────────────────────────────────────────────┐
│                      Feature Layer                     │
│               (Smart Container Components)             │
└──────────────────────────┬─────────────────────────────┘
                           │ Dispatches / Invokes
                           ▼
┌────────────────────────────────────────────────────────┐
│                      State Layer                       │
│             (NgRx Store / Signal Stores)               │
└──────────────────────────┬─────────────────────────────┘
                           │ Triggers HTTP
                           ▼
┌────────────────────────────────────────────────────────┐
│                   Data Access Layer                    │
│             (API Services / DTO Models / Mappers)      │
└────────────────────────────────────────────────────────┘
```

## How does it work?
1. **Domain-Driven Design (DDD)**: Partitions the application into isolated business domains (e.g., `billing`, `inventory`, `analytics`, `auth`). Each domain encapsulates its own features, data access, state, and UI components.
2. **Smart Components (Containers)**: Coordinate application behavior, inject services or stores, manage state subscriptions, and handle routing parameters.
3. **Dumb Components (Presentational)**: Pure UI widgets that receive immutable data via inputs (`@Input()` or `input()`), emit user interaction events via outputs (`@Output()` or `output()`), and have zero dependencies on backend services or store singletons.
4. **Layered Architectural Slicing**:
   - **`core/`**: Application-wide singletons initialized at bootstrap (Authentication services, Guards, Interceptors, Global Configuration).
   - **`shared/`**: Generic, domain-agnostic UI primitives (Custom Buttons, Data Table wrappers, Modal containers, Loading Spinners).
   - **`domains/` (or `features/`)**: Business-specific modules containing domain models, state stores, and feature pages.

## Impact
* **Application Architecture**: Prevents tight coupling across functional areas, making code discovery and refactoring predictable.
* **Performance**: Clean domain boundaries make lazy loading and route-based code splitting natural and automated.
* **Scalability**: Enables multiple independent squads to work concurrently on separate business domains within an Nx monorepo without merge conflicts or code regressions.

## Real World Example
In an enterprise retail platform, the `customer-support` domain and the `checkout-payments` domain reside in isolated domain libraries. The payments team can upgrade payment gateways or refactor checkout form flows without impacting or requiring regression testing on customer support features.

## Syntax
Standard enterprise directory structure:

```
src/
├── app/
│   ├── core/                  # Global singletons (Auth, Interceptors, Route Guards)
│   ├── shared/                # Domain-agnostic UI components, pipes, directives
│   │   ├── ui/                # Buttons, Cards, Modals
│   │   └── utils/             # Formatters, helpers
│   └── domains/               # Business Domain Modules
│       ├── billing/           # Billing Domain
│       │   ├── data-access/   # API services, DTOs, interfaces
│       │   ├── state/         # NgRx Store / Signal Store
│       │   ├── features/      # Smart page containers (InvoiceList, Checkout)
│       │   └── ui/            # Presentational dumb components (InvoiceCard)
│       └── catalog/           # Catalog Domain
```

## Code Examples
Below is a complete implementation demonstrating the **Smart / Dumb Component** architectural pattern:

### `product-card.component.ts` (Dumb / Presentational Component)
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
  changeDetection: ChangeDetectionStrategy.OnPush, // High performance through immutability
  template: `
    <div class="card">
      <h4>{{ product.title }}</h4>
      <p class="price">Price: {{ product.price | currency }}</p>
      
      <!-- Emit events up to the smart parent container -->
      <button (click)="select.emit(product)">View Details</button>
    </div>
  `,
  styles: [`
    .card { 
      border: 1px solid #d1d5db; 
      padding: 16px; 
      border-radius: 8px; 
      background: white; 
    }
    .price { font-weight: bold; color: #059669; }
    button { padding: 6px 12px; background: #2563eb; color: white; border: none; border-radius: 4px; cursor: pointer; }
  `]
})
export class ProductCardComponent {
  // Receives immutable data from parent smart container
  @Input({ required: true }) product!: ProductItem;
  
  // Emits user interaction events upward
  @Output() select = new EventEmitter<ProductItem>();
}
```

### `product-catalog.component.ts` (Smart / Container Component)
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
        <!-- Dumb components handle UI presentation -->
        @for (item of products(); track item.id) {
          <app-product-card 
            [product]="item" 
            (select)="handleProductSelect($event)">
          </app-product-card>
        }
      </div>

      @if (selectedProduct(); as product) {
        <div class="selection-drawer">
          <p>Selected Product: <strong>{{ product.title }}</strong> ({{ product.price | currency }})</p>
        </div>
      }
    </div>
  `,
  styles: [`
    .catalog-container { padding: 24px; font-family: sans-serif; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
    .selection-drawer { margin-top: 24px; background: #eff6ff; border: 1px solid #bfdbfe; padding: 16px; border-radius: 6px; }
  `]
})
export class ProductCatalogComponent implements OnInit {
  private http = inject(HttpClient);

  // Manages state, async loading, and business decisions
  products = signal<ProductItem[]>([]);
  selectedProduct = signal<ProductItem | null>(null);

  ngOnInit(): void {
    this.http.get<ProductItem[]>('https://api.escuelajs.co/api/v1/products?limit=6')
      .subscribe(data => this.products.set(data));
  }

  handleProductSelect(product: ProductItem): void {
    this.selectedProduct.set(product);
  }
}
```

## Best Practices
1. **Strictly Enforce Smart / Dumb Component Separation**: Keep presentational components clean of services, APIs, and routing dependencies. Use only inputs and outputs.
2. **Organize by Business Domain**: Group related components, services, and state models into domain folders (`domains/orders`, `domains/customers`) instead of grouping by technical type (`components/`, `services/`).
3. **Configure Monorepo Boundary Rules (Nx Lint Rules)**: If using an Nx Monorepo, enforce module boundary tags (e.g., `scope:orders`, `type:ui`) to prevent cross-domain imports and enforce unidirectional dependency flow.

## Common Mistakes
* **Injecting Services Directly into Dumb Components**: Injecting state stores or `HttpClient` inside presentational widgets tightly couples them to a specific backend context, preventing reusability.
* **Bloating the Shared Directory**: Dumping feature-specific code into `shared/`. Keep `shared/` strictly for generic UI components and utility functions used across multiple domains.

## Interview Questions & Answers
### Q: What is the difference between a Smart Component and a Dumb Component?
**A**: **Smart Components** (Containers) manage state, inject services, make HTTP requests, interact with stores, and handle routing parameters. **Dumb Components** (Presentational) are pure UI rendering widgets; they have no injected business services, receive data strictly via inputs, and notify parent containers via outputs, making them highly reusable and easy to unit test.

### Q: Why is Domain-Driven Design (DDD) recommended for large enterprise Angular applications?
**A**: Domain-Driven Design organizes code around discrete business domains (e.g., `orders`, `billing`, `inventory`) rather than technical file types. This eliminates tight coupling between unrelated application areas, enables smooth lazy loading of entire domains, and allows independent engineering teams to develop and deploy features concurrently without code conflicts.

## Summary
Enterprise Angular architecture relies on Domain-Driven Design, clean layered boundaries, and the Smart/Dumb component pattern. Isolating business state from presentation views ensures enterprise codebases remain scalable, modular, and maintainable over time.

---

Previous : [SSR and Advanced Concepts](./24_SSR_and_Advanced_Concepts.md) | Index : [Home](./00_index.md) | Next : [Deployment and CI/CD](./26_Deployment_and_CI_CD.md)
