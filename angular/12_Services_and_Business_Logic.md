# Services and Business Logic

## What is it?
A Service is a class decorated with `@Injectable` that encapsulates non-UI logic. It forms the business logic layer of your application, managing tasks like API calls, calculations, state tracking, and data persistence.

## Why do we need it?
Components should only be responsible for displaying data and handling user interactions. If you write data processing, calculation, or HTTP request logic inside component files, they become bloated, hard to test, and duplicate code. Services solve this by encapsulating business logic in reusable, testable classes that can be injected anywhere.

```
M-V-S Architecture:
Component (View Presentation) <─── (Observable/Signal updates) ─── Service (Business Logic Layer)
                                                                     │
                                                                     ▼
                                                             External APIs / DB
```

## How does it work?
1. **Singleton Lifecycle**: By default, decorating a service with `@Injectable({ providedIn: 'root' })` registers it as a global singleton. When injected into multiple components, they all share the same instance and state.
2. **Transient Lifecycle**: If registered in a component's `providers: [...]` array, Angular creates a new instance of the service for that component, destroying it when the component is removed from the DOM.
3. **Decoupled Architecture**: Components query the service for data, and the service manages calculations or fetches new data over the network.

## Impact
* **Application Architecture**: Creates a clean separation between the presentation layer (components) and the data/business logic layer (services).
* **Performance**: Shared singletons prevent duplicate network requests and conserve memory.
* **Maintainability**: Changing business logic or API endpoints only requires updating the service file, leaving components untouched.

## Real World Example
In a financial dashboard, a `CurrencyExchangeService` periodically fetches conversion rates from a server. Multiple components (checkout, billing, catalog) inject this service to convert currencies without running separate network timers.

## Syntax
A standard service setup:
```typescript
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root' // Singleton declaration
})
export class ProductService {
  private http = inject(HttpClient);

  getProducts() {
    return this.http.get('/api/products');
  }
}
```

## Hinglish Explanation

Angular me Components ko **"Waiter"** aur Services ko **"Kitchen/Chef"** ki tarah samajhein.
* **Component (Waiter):** Yeh customer (user) se order leta hai aur screen par display dikhata hai (presentation logic). Isko actual computations (business logic ya API calls) nahi karni chahiye.
* **Service (Chef/Kitchen):** Yeh kitchen me back-end operations karta hai (data fetch karna, calculations karna, database transactions). Waiter sirf Chef se raw material ya prepared data lekar UI par render kar deta hai.

### 1. Services Kyun Zaroori Hain?
* **Code Reusability:** Agar product list fetch karne ka logic do alag-alag pages (dashboard aur search) me chahiye, toh hum use components ke andar duplicate karne ke bajaye ek common Service me likhte hain aur dono components me inject kar lete hain.
* **Clean Code:** Service use karne se component file choti aur simple rehti hai, jisse code readable aur maintainable banta hai.

### 2. Service Kaise Banate Hain?
Service banane ke liye `@Injectable()` decorator ka use hota hai:
```typescript
@Injectable({
  providedIn: 'root' // Matlab poore app me ek hi copy share hogi (Singleton)
})
export class ProductService {
  // Business logic & HTTP calls yahan hote hain
}
```

## Code Examples
Below is a complete implementation of a shared state service managing a shopping cart.

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

  // Computed signals exposed to components
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
    .catalog { border: 1px solid #d1d5db; padding: 20px; border-radius: 6px; }
  `]
})
export class ProductCatalogComponent {
  // Inject the CartService singleton
  cart = inject(CartService);

  addProduct() {
    const laptop: CartItem = {
      id: Math.random().toString(),
      name: 'Developer Laptop',
      price: 1499.00
    };
    this.cart.addToCart(laptop);
  }
}
```

## Best Practices
1. **Delegation**: Components should remain thin. If a component method contains more than 10-15 lines of logic or calculations, consider delegating it to a service.
2. **Read-Only State**: Do not expose writable signals or RxJS Subjects directly from services. Expose them as read-only computed signals or observables.
3. **Encapsulate HTTP logic**: Keep raw `HttpClient` requests inside services. Do not call endpoints directly from component files.

## Common Mistakes
* **Storing Local UI State globally**: Using a shared singleton service to track UI-specific state, like whether a sidebar is open in an individual component, which can affect other instances of the component.
* **Forgetting the `@Injectable()` Decorator**: Creating a service class without the `@Injectable()` decorator. This prevents the class from receiving other DI dependencies, throwing errors during compilation.

## Interview Questions & Answers
### Q: How do you implement a singleton service in Angular?
**A**: Decorate the service class with `@Injectable({ providedIn: 'root' })`. This registers the service with the root injector, making a single, shared instance available application-wide.
* **Hinglish Explanation**: Singleton service banane ke liye, service class ke upar `@Injectable({ providedIn: 'root' })` decorator lagaya jata hai. Isse yeh service globally root level par register ho jati hai aur pure application me iski sirf ek hi single shared copy (instance) use hoti hai.

### Q: Why is it bad practice to write calculations or HTTP operations inside components?
**A**: Writing calculations or HTTP operations inside components violates the Single Responsibility Principle, makes testing difficult, and leads to duplicate code. Delegating these tasks to services keeps components focused on presentation.
* **Hinglish Explanation**: Components ka kaam hota hai sirf screen par layout dikhana aur events capture karna. Agar aap business logic ya HTTP operations components me likhoge, toh code ganda (complex) ho jayega aur usey reuse ya test karna bohot mushkil ho jayega. Services me data calculations rakhne se components clean rehte hain aur hum ek hi service logic ko different components me easily reuse kar sakte hain.

## Summary
Services contain your application's business and data logic. Global singletons are declared using `@Injectable({ providedIn: 'root' })`, separating data management from presentation component files.

---

Previous : [Dependency Injection](./11_Dependency_Injection.md) | Index : [Home](./00_index.md) | Next : [Routing and Navigation](./13_Routing_and_Navigation.md)
