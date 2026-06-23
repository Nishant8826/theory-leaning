# Services and Business Logic

## What is it?
Service ek normal class hoti hai jise `@Injectable` decorator se decorate kiya jata hai aur yeh non-UI logic ko encapsulate karti hai. Yeh aapke application ki business logic layer banati hai, jo tasks jaise API calls, calculations, state management, aur data persistence (local storage) ko control karti hai.

## Why do we need it?
Components ka kaam sirf data show karna aur user interactions handle karna hona chahiye. Agar aap data processing, mathematical calculations, ya direct API integration requests component files me likhenge, toh class code bohot bada aur chaotic ho jayega. Services is problem ko reusable, testable classes me business logic wrap karke solve karti hain jinhe kahin bhi inject kiya ja sakta hai.

```
M-V-S Architecture:
Component (View Presentation) <─── (Observable/Signal updates) ─── Service (Business Logic Layer)
                                                                     │
                                                                     ▼
                                                              External APIs / DB
```

## How does it work?
1. **Singleton Lifecycle**: By default, service ke upar `@Injectable({ providedIn: 'root' })` register karne se yeh global singleton ban jati hai. Jab hum ise multiple components me inject karte hain, toh sabhi components same single copy aur active status values share karte hain.
2. **Transient Lifecycle**: Agar service ko component metadata array `providers: [...]` me register kiya jaye, toh Angular us specific component ke liye ek naya custom instance generate karega aur component destroy hone par us service object copy ko destroy kar dega.
3. **Decoupled Architecture**: Components data fetch ya actions updates ke liye service variables ya methods call karte hain aur service background calculations aur computations coordinate karti hai.

## Impact
* **Application Architecture**: View presentation (components) aur core calculations layer (services) ke beech clean separation create karta hai.
* **Performance**: Shared singletons duplicate background network requests control karte hain aur RAM memory optimize rakhte hain.
* **Maintainability**: API endpoints updates ya calculations formula change karne ke liye components code edit nahi karna padta, sirf service file code update karna padta hai.

## Real World Example
Fintech portal website me, `CurrencyExchangeService` periodically backend service se current conversion rates updates load karti hai. Checkout page, profile options, ya invoice bill details component direct is service ko inject kar rates read kar lete hain bina unique network request trigger kiye.

## Syntax
Ek standard service layout design setup:
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

## Code Examples
Shopping cart data manage karne wali stateful service ka standalone implementation demo setup:

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
1. **Delegation**: Components code layout lightweight rakhein. Agar component method logic 10-15 lines se badhne lage, toh use helper service function me transfer karein.
2. **Read-Only State**: Public services variables me direct modification inputs block karein. Signals ya RxJS streams ko components interface ke liye read-only formats (`asReadonly()`, `asObservable()`) me expose karein.
3. **Encapsulate HTTP logic**: Saare network routes request details services file me locate rakhein, component file methods me endpoints parameters hardcode na karein.

## Common Mistakes
* **Storing Local UI State globally**: Sibling components dynamic flags (jaise sidebar toggle status check) global singleton service me maintain karna, jo other views behaviors conflict kar sakta hai.
* **Forgetting the `@Injectable()` Decorator**: Custom service class ke upar `@Injectable()` decoration remove rakhna. Isse components inject system service dependencies inject nahi kar pata aur build errors aate hain.

## Interview Questions & Answers
### Q: How do you implement a singleton service in Angular?
**A**: Service class definition ke upar `@Injectable({ providedIn: 'root' })` tag declare karein. Isse root injector setup dynamic memory me application-wide single instance configure kar deta hai.

### Q: Why is it bad practice to write calculations or HTTP operations inside components?
**A**: Calculation aur HTTP variables components me likhna Single Responsibility Principle violation hai aur data reuse restrictions badhata hai. Services use karne se UI code clean aur scalable rehta hai.

## Summary
Services application core business calculations aur API requests handle karti hain. `@Injectable({ providedIn: 'root' })` decorator global singleton configuration handle karta hai jisse visual components and logic codes beautifully manage hote hain.

---

Previous : [Dependency Injection](./11_Dependency_Injection.md) | Index : [Home](./00_index.md) | Next : [Routing and Navigation](./13_Routing_and_Navigation.md)
