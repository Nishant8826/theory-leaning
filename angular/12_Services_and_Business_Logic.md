# Services and Business Logic

## What is it?
A Service in Angular is a TypeScript class decorated with `@Injectable()` designed to encapsulate non-UI business logic, application state, data calculations, external API communication, and local persistence (e.g., LocalStorage or IndexedDB).

## Why do we need it?
Components should focus strictly on presenting the user interface and handling direct user interactions. Writing raw HTTP calls, mathematical computations, or complex data manipulation directly inside component classes creates bloated, unmaintainable code and leads to severe duplication across views. 

Services solve this by extracting business logic into reusable, testable, and injectable singletons that can be shared across any component in the application.

```
Model-View-Service (MVS) Architecture:
Component (UI Presentation) <─── (Observable/Signal updates) ─── Service (Business Logic Layer)
                                                                     │
                                                                     ▼
                                                              External APIs / DB
```

## How does it work?
1. **Singleton Lifecycle**: Decorating a service with `@Injectable({ providedIn: 'root' })` registers it with the root injector as a global singleton. Every component that injects this service receives the exact same shared instance and synchronized state.
2. **Scoped Lifecycle**: Registering a service within a component's `providers: [...]` array creates a dedicated instance for that component branch. When the component is destroyed, Angular destroys the scoped service instance.
3. **Decoupled Coordination**: Components invoke service methods to trigger actions or read reactive state (Signals or Observables), while the service handles validation, data transformations, and HTTP integration behind the scenes.

## Impact
* **Application Architecture**: Establishes a clean separation between UI presentation (components) and business logic/data access (services).
* **Performance**: Shared singletons prevent duplicate HTTP calls, minimize memory allocations, and enable clean reactive state distribution.
* **Maintainability**: Changing an API URL or updating a tax calculation formula requires editing only the service, leaving all consuming components untouched.

## Real World Example
In a fintech trading portal, a `CurrencyExchangeService` periodically fetches real-time currency exchange rates from a backend API. The checkout page, billing invoice modal, and user wallet components all inject this single service to read live rates without triggering multiple redundant network requests.

## Syntax
Basic injectable service definition:

```typescript
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root' // Singleton registration
})
export class ProductService {
  private http = inject(HttpClient);

  getProducts(): Observable<Product[]> {
    return this.http.get<Product[]>('/api/products');
  }
}
```

## Code Examples
Below is a complete implementation of a reactive, signal-based shopping cart service and a consuming catalog component:

### `cart.service.ts`
```typescript
import { Injectable, signal, computed } from '@angular/core';

export interface CartItem {
  id: string;
  name: string;
  price: number;
}

@Injectable({
  providedIn: 'root'
})
export class CartService {
  // Writable signal tracking items list (private to prevent external mutations)
  private cartItems = signal<CartItem[]>([]);

  // Computed signals exposed as read-only properties to components
  items = computed(() => this.cartItems());
  itemCount = computed(() => this.cartItems().length);
  totalPrice = computed(() => this.cartItems().reduce((acc, curr) => acc + curr.price, 0));

  addToCart(item: CartItem): void {
    this.cartItems.update(current => [...current, item]);
  }

  removeFromCart(itemId: string): void {
    this.cartItems.update(current => current.filter(x => x.id !== itemId));
  }

  clearCart(): void {
    this.cartItems.set([]);
  }
}
```

### `product-catalog.component.ts`
```typescript
import { Component, inject } from '@angular/core';
import { CartService, CartItem } from './cart.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-product-catalog',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="catalog">
      <h3>Store Catalog</h3>
      <button (click)="addProduct()">Add Laptop to Cart</button>
      
      <div class="summary">
        <p>Items in Cart: {{ cart.itemCount() }}</p>
        <p>Total Price: {{ cart.totalPrice() | currency }}</p>
      </div>
    </div>
  `,
  styles: [`
    .catalog { 
      border: 1px solid #d1d5db; 
      padding: 20px; 
      border-radius: 6px; 
      max-width: 320px;
      font-family: sans-serif;
    }
    button {
      padding: 8px 16px;
      background-color: #2563eb;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    .summary {
      margin-top: 15px;
      font-weight: bold;
    }
  `]
})
export class ProductCatalogComponent {
  cart = inject(CartService);

  addProduct(): void {
    const laptop: CartItem = {
      id: Math.random().toString(),
      name: 'Developer Laptop Pro',
      price: 1499.00
    };
    this.cart.addToCart(laptop);
  }
}
```

## Best Practices
1. **Delegate Logic Immediately**: Keep component classes slim and presentational. If a component method exceeds 10–15 lines of business calculations, delegate that logic to a dedicated service.
2. **Encapsulate State with Read-Only Signals/Streams**: Keep internal writable state private (`private cartItems = signal<CartItem[]>([])`). Expose state to components only through computed signals or read-only observables (`asReadonly()`).
3. **Encapsulate HTTP Requests**: Isolate all API endpoints, parameters, and error handlers within services. Never write raw `HttpClient` calls directly inside component files.

## Common Mistakes
* **Storing Component-Specific UI State Globally**: Storing transient UI state (such as whether a local accordion panel is open) inside a global singleton service, causing unintended state side effects across views.
* **Missing `@Injectable()` Decorator**: Forgetting to add the `@Injectable()` decorator on a service class. Without it, Angular's DI injector cannot resolve constructor dependencies or inject the service properly.

## Interview Questions & Answers
### Q: How do you implement a Singleton Service in Angular?
**A**: Add the `@Injectable({ providedIn: 'root' })` decorator to the service class. This instructs Angular's root injector to create a single application-wide instance that is lazily loaded and tree-shakable.

### Q: Why is it considered an anti-pattern to perform HTTP calls or heavy computations directly inside components?
**A**: Placing HTTP operations and heavy computations inside components violates the Single Responsibility Principle (SRP). It couples the UI presentation tightly with the data access layer, prevents reusability across other components, and makes automated unit testing cumbersome and error-prone.

## Summary
Services encapsulate application business logic, calculations, state, and HTTP operations. Using `@Injectable({ providedIn: 'root' })` establishes tree-shakable global singletons, ensuring a clean separation between UI presentation and core application logic.

---

Previous : [Dependency Injection](./11_Dependency_Injection.md) | Index : [Home](./00_index.md) | Next : [Routing and Navigation](./13_Routing_and_Navigation.md)
