# Real World E-Commerce Project

## What is it?
Real-World E-Commerce Project design specification us architecture, routing, state, aur deployment configurations ko define karta hai jiske zariye ek scalable shop application build kiya jata hai. Yeh production environments me features aur data flows ko organize karne ke liye ek practical guide ki tarah kaam kaam karta hai.

## Why do we need it?
Individual features ko alag-alag seekhna zaroori hai, par ek production application build karne ke liye unhe ek cohesive structure me combine karna padta. Ek mock application (jaise e-commerce platform) design karne se yeh samajh aata hai ki routing tables ko kaise structure karein, shared state (jaise shopping carts aur authentication) ko kaise manage karein, APIs ko kaise configure karein, aur deployment pipelines ko kaise set up karein.

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
1. **Folder Layout**: Domain-driven structure ka use karta hai (`core`, `shared`, `domains/cart`, `domains/catalog`).
2. **Routing Structure**: Domain features (jaise `/catalog`, `/cart`, aur `/checkout`) ko lazy-load karta hai aur checkout paths ko secure karne ke liye functional guards ka use karta hai.
3. **State Management**: Cart items aur user sessions ko manage karne ke liye `NgRx Signal Store` ya shared services ka use karta hai.
4. **API Integration**: `HttpClient` aur functional interceptors ka use karke REST APIs ke sath integrate karta hai taaki authorization tokens automatically append ho sakein.
5. **Deployment Configuration**: Production assets ko compile karta hai aur cloud environments par Nginx/Docker containers me host karta hai.

## Impact
* **Application Architecture**: Tight coupling ko rokta hai, jisse features ko scale aur refactor karna easy ho jata hai.
* **Performance**: Lazy loading aur state caching page transitions ko smooth aur load times ko fast rakhte hain.
* **Scalability**: Feature boundaries ko clean rakhta hai, jisse multiple teams independent tarike se features develop kar sakti hain.

## Real World Example
Ek commercial e-commerce platform me, catalog team search filters aur details layouts ko update karti hai jabki payments team checkout integrations par kaam karti hai. Isse dono teams bina kisi merge conflicts ke updates ko independently release kar sakti hain.

## Syntax
E-commerce platform ke liye ek enterprise-grade folder structure:
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
Neeche e-commerce project ke liye key architectural configurations diye gaye hain.

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
1. **Always lazy-load domains**: Route views ko configure karein taaki unke code bundles on-demand dynamically loading process run karein using `loadComponent`.
2. **Secure routes with functional guards**: Secure checkout paths ko configure karne ke liye functional guards ka use karein, jo status fail hone par user ko `/login` par redirect kar dein.
3. **Isolate domain boundaries**: Kisi domain folder ke andar dusre domain ke private files ya helpers ko reference na karein. Shared interfaces ko core directory me hi rakhein.

## Common Mistakes
* **Monolithic state models**: Catalog, billing, aur layout configurations ko ek hi single store me manage karna. State ko separate domain stores (jaise `CartStore`, `UserStore`) me divide karein.
* **Statically importing feature bundles**: Configuration files me route components ko statically import karna. Isse unke code bundles main bundle size me add ho jate hain, jisse initial page load slow ho jata hai.

## Interview Questions & Answers
### Q: How would you design a shopping cart state in a large Angular e-commerce application?
**A**: E-commerce cart state ko design karne ke liye main ek functional `CartStore` (using NgRx Signal Store API) develop karunga jise global singleton register kiya jayega. Yeh store current items list ko hold karega aur computed signals ke zariye automatic subtotal, shipping charges, aur grand total dynamically calculate karega. Isse UI automatic update hogi aur data presentation files se separate rahega.

### Q: Why is the separation of public catalog routes and secure checkout routes important?
**A**: Lead updates coordinates security aur performance dono ke liye zaroori hai. Public catalog route ko har user access kar sakta hai aur iska bundle turant render hota hai. Checkout route par hum authentication route guards lagate hain. Isse unauthorized users secure checkout page/payment codes aur JS bundles ko download nahi kar paate, jisse overall page startup load time reduce hota hai.

## Summary
Enterprise e-commerce design lazy-loaded domains, functional guards (`CanActivateFn`), aur global state configurations (`CartStore`) ka leverage karta hai taaki ek fast, secure, aur maintainable shopping application build kiya ja sake.

---

Previous : [Deployment and CI/CD](./26_Deployment_and_CI_CD.md) | Index : [Home](./00_index.md) | Next : [Beginner Interview Prep](./28_Interview_Prep_Beginner.md)
