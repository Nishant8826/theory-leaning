# Real World E-Commerce Project

## What is it?
The Real-World E-Commerce Project design specification defines the architecture, routing, state, and deployment configurations used to build a scalable shop application. It serves as a practical guide for organizing features and data flows in production environments.

## Why do we need it?
While learning individual features in isolation is useful, building a production application requires combining them into a cohesive structure. Designing a mock application (like an e-commerce platform) shows how to structure routing tables, manage shared state (such as shopping carts and authentication), configure APIs, and set up deployment pipelines.

```
E-Commerce Architecture Overview:
                     ┌──────────────────────────────────┐
                     │          App Routes              │
                     │  (Lazy Loaded Domain Bundles)    │
                     └──────────────┬───────────────────┘
                                    ▼
       ┌────────────────────────────┼────────────────────────────┐
       ▼                            ▼                            ▼
┌──────────────┐             ┌──────────────┐             ┌──────────────┐
│ Auth Domain  │             │ Catalog/Cart │             │ Checkout     │
│ (Login/JWT)  │             │ (Signals)    │             │ (Forms/Auth) │
└──────────────┘             └──────────────┘             └──────────────┘
```

## How does it work?
1. **Folder Layout**: Uses a domain-driven structure (`core`, `shared`, `domains/cart`, `domains/catalog`).
2. **Routing Structure**: Lazy-loads domain features (like `/catalog`, `/cart`, and `/checkout`) and uses functional guards to secure checkout paths.
3. **State Management**: Uses the `NgRx Signal Store` or shared services to manage cart items and user sessions.
4. **API Integration**: Integrates with REST APIs using `HttpClient` and functional interceptors to append authorization tokens automatically.
5. **Deployment Configuration**: Compiles production assets and hosts them in Nginx/Docker containers on cloud environments.

## Impact
* **Application Architecture**: Prevents tight coupling, making features easy to scale and refactor.
* **Performance**: Lazy loading and state caching keep page transitions smooth and load times fast.
* **Scalability**: Keeps feature boundaries clean, allowing multiple teams to develop features independently.

## Real World Example
In a commercial e-commerce platform, the catalog team updates search filters and details layouts while the payments team works on checkout integrations, allowing both teams to release updates independently without merge conflicts.

## Syntax
An enterprise-grade folder structure for an e-commerce platform:
```
src/app/
├── core/                  # Core singletons (JWT, interceptors, guards)
├── shared/                # Shared UI controls (Buttons, inputs, spinners)
└── domains/               # Domain boundaries
    ├── catalog/           # Catalog domain (search, detail views)
    ├── cart/              # Cart domain (item models, checkout states)
    └── checkout/          # Checkout domain (payment gateways, address forms)
```

## Code Examples
Below are the key architectural configurations for the e-commerce project.

### `app.routes.ts` (Routing Layout)
```typescript
import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  // 1. Public catalog list
  {
    path: 'catalog',
    loadComponent: () => import('./domains/catalog/features/catalog-list/catalog-list.component')
      .then(m => m.CatalogListComponent)
  },
  // 2. Public product detail
  {
    path: 'product/:id',
    loadComponent: () => import('./domains/catalog/features/product-detail/product-detail.component')
      .then(m => m.ProductDetailComponent)
  },
  // 3. Shared shopping cart view
  {
    path: 'cart',
    loadComponent: () => import('./domains/cart/features/cart-view/cart-view.component')
      .then(m => m.CartViewComponent)
  },
  // 4. Secure checkout path
  {
    path: 'checkout',
    canActivate: [authGuard], // Secured path
    loadComponent: () => import('./domains/checkout/features/checkout-flow/checkout-flow.component')
      .then(m => m.CheckoutFlowComponent)
  },
  { path: '', redirectTo: '/catalog', pathMatch: 'full' },
  { path: '**', redirectTo: '/catalog' }
];
```

### `cart.store.ts` (Cart State Configuration)
```typescript
import { signalStore, withState, withMethods, patchState, withComputed } from '@ngrx/signals';
import { computed } from '@angular/core';

export interface CartItem {
  id: string;
  title: string;
  price: number;
  qty: number;
}

export interface CartState {
  items: CartItem[];
  shippingFee: number;
}

const initialState: CartState = {
  items: [],
  shippingFee: 15.00
};

export const CartStore = signalStore(
  { providedIn: 'root' },
  withState(initialState),
  withComputed(({ items, shippingFee }) => ({
    itemCount: computed(() => items().reduce((acc, item) => acc + item.qty, 0)),
    subtotal: computed(() => items().reduce((acc, item) => acc + (item.price * item.qty), 0)),
    total: computed(() => items().reduce((acc, item) => acc + (item.price * item.qty), 0) + shippingFee())
  })),
  withMethods((store) => ({
    addItem(product: Omit<CartItem, 'qty'>) {
      const currentItems = store.items();
      const existing = currentItems.find(x => x.id === product.id);

      if (existing) {
        // Increment quantity if item exists
        patchState(store, {
          items: currentItems.map(x => x.id === product.id ? { ...x, qty: x.qty + 1 } : x)
        });
      } else {
        // Add new item to array
        patchState(store, {
          items: [...currentItems, { ...product, qty: 1 }]
        });
      }
    },
    removeItem(itemId: string) {
      patchState(store, {
        items: store.items().filter(x => x.id !== itemId)
      });
    }
  }))
);
```

## Best Practices
1. **Always lazy-load domains**: Configure route views to lazy-load their code bundles on-demand using `loadComponent`.
2. **Secure routes with functional guards**: Secure checkout paths using functional guards that redirect users to `/login` if auth checks fail.
3. **Isolate domain boundaries**: Do not import private helpers or data models across unrelated domain folders. Keep shared interfaces in the core directory.

## Common Mistakes
* **Monolithic state models**: Managing catalog, billing, and layout configurations inside a single store. Break state down into separate domain stores (e.g. `CartStore`, `UserStore`).
* **Statically importing feature bundles**: Importing route components statically in configuration files. This includes their code bundles in the main bundle size, causing slower initial page loads.

## Interview Questions & Answers
### Q: How would you design a shopping cart state in a large Angular e-commerce application?
**A**: I would design the cart state using a functional `CartStore` (via the NgRx Signal Store API) registered as a global singleton. It would expose computed signals for subtotal, shipping fee, and grand total. This enables fast, reactive UI updates and separates shopping cart data from presentation components.

### Q: Why is the separation of public catalog routes and secure checkout routes important?
**A**: It is important because it keeps the checkout bundle secure. Public routes (like catalog and details) load immediately without validation checks, while secure checkout routes are guarded using auth guards that prevent unauthorized users from downloading billing files or checkout bundles.

## Summary
The enterprise e-commerce design leverages lazy-loaded domains, functional guards (`CanActivateFn`), and global state configurations (`CartStore`) to build a fast, secure, and maintainable shopping application.

---

Previous : [Deployment and CI/CD](./26_Deployment_and_CI_CD.md) | Index : [Home](./00_index.md) | Next : [Beginner Interview Prep](./28_Interview_Prep_Beginner.md)
