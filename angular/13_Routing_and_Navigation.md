# Routing and Navigation

## What is it?
Routing ek aisa mechanism hai jo browser ke URL paths ko dynamic components ke sath map karta. Yeh Single Page Applications (SPAs) ko user navigation par index file refresh ya page reload kiye bina dynamic views render karne me enable karta hai.

## Why do we need it?
Traditional websites me jab user kisi hyperlink text par click karta hai, toh har path navigate event par browser complete HTML page server se download karta hai jisse site load behavior slow ho jata hai. SPA apps me Single document render model target hota hai, browser URL transition detect hone par dynamic components swaps load process coordinate kar leta hai.

```
Routing Flow:
URL Change (/products/4) ──> Router evaluates path ──> Resolves lazy components
                          ──> Runs Guards (Auth check) ──> Loads data via Resolver
                          ──> Renders ProductDetailsComponent inside <router-outlet>
```

## How does it work?
1. **Route Definitions**: Path string aur matching component links ka ek configuration mappings array.
2. **Router Outlet (`<router-outlet>`)**: Ek directive container placeholder coordinate jahan dynamic router component instances load hokar render hote hain.
3. **Lazy Loading (`loadComponent`)**: Main app bundle files ko domains chunks me dynamically divide karna, jisse page initialization startup speeds optimize ho jati hain.
4. **Guards (CanActivate, CanMatch)**: Functional checkpoints logic jo authentication parameters check karke path access block ya open karte hain.
5. **Resolvers**: Web rendering page startup delay prevent karne ke liye dynamic component render access se pehle backend request data values pre-load framework logic run karna.

## Impact
* **Application Architecture**: Web pages links pathways definitions layout mapping clear rakhta hai.
* **Performance**: Lazy loading route components page bundles coordinate speed increase karte hain.
* **Scalability**: Child routes nested navigation routes setup components code management structure standard maintain rakhta hai.

## Real World Example
E-commerce application settings admin dashboard link navigate check trigger hone par functional route guard check run hota hai. Agar validation complete hai, tabhi admin bundle download access load configuration command active hoti hai.

## Syntax
* **Route Configuration**:
```typescript
{ path: 'products/:id', loadComponent: () => import('./detail.component').then(m => m.DetailComponent) }
```
* **RouterLink Navigation**:
```html
<a routerLink="/products/12" [queryParams]="{ ref: 'email' }">View Product</a>
```
* **Imperative Navigation**:
```typescript
this.router.navigate(['/products', 12], { queryParams: { ref: 'email' } });
```

## Code Examples
Neeche child routes, lazy loading, parameters, aur modern functional guards ka complete implementation diya gaya hai:

### `app.routes.ts`
```typescript
import { Routes, Router, CanActivateFn } from '@angular/router';
import { inject } from '@angular/core';

// 1. Define a Functional Auth Guard
export const authGuard: CanActivateFn = () => {
  const router = inject(Router);
  const isLoggedIn = !!localStorage.getItem('token'); // Mock authentication check
  return isLoggedIn ? true : router.createUrlTree(['/login']);
};

// 2. Main Route Configuration
export const routes: Routes = [
  { path: 'login', loadComponent: () => import('./login.component').then(m => m.LoginComponent) },
  {
    path: 'admin',
    canActivate: [authGuard],
    // Lazy loaded feature parent
    loadComponent: () => import('./admin-panel.component').then(m => m.AdminPanelComponent),
    children: [
      {
        path: 'users',
        loadComponent: () => import('./admin-users.component').then(m => m.AdminUsersComponent)
      },
      {
        path: 'settings',
        loadComponent: () => import('./admin-settings.component').then(m => m.AdminSettingsComponent)
      }
    ]
  },
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: '**', loadComponent: () => import('./not-found.component').then(m => m.NotFoundComponent) }
];
```

### `admin-panel.component.ts`
```typescript
import { Component, inject } from '@angular/core';
import { Router, RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-admin-panel',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="admin-layout">
      <nav class="sidebar">
        <a routerLink="users" routerLinkActive="active-link">Manage Users</a> |
        <a routerLink="settings" routerLinkActive="active-link">Settings</a>
        <button (click)="logout()">Log Out</button>
      </nav>
      <main class="content">
        <router-outlet></router-outlet>
      </main>
    </div>
  `,
  styles: [`
    .admin-layout { display: flex; font-family: sans-serif; }
    .sidebar { width: 200px; padding: 20px; background: #f3f4f6; }
    .active-link { font-weight: bold; color: #3b82f6; }
    .content { flex: 1; padding: 20px; }
  `]
})
export class AdminPanelComponent {
  private router = inject(Router);

  logout() {
    localStorage.removeItem('token');
    this.router.navigate(['/login']);
  }
}
```

### Unrelated Components Communication (Using Shared Services)

**Method 1: Using `ActivatedRoute` (Traditional)**
```typescript
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-user-detail',
  template: `<p>User ID: {{ userId }} | Search: {{ searchVal }}</p>`
})
export class UserDetailComponent implements OnInit {
  userId: string | null = null;
  searchVal: string | null = null;

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      this.userId = params.get('id');
    });

    this.route.queryParamMap.subscribe(params => {
      this.searchVal = params.get('search');
    });
  }
}
```

**Method 2: Using Component Input Binding (Angular 16+)**

1. Enable `withComponentInputBinding()` in `app.config.ts`:
```typescript
import { provideRouter, withComponentInputBinding } from '@angular/router';
import { routes } from './app.routes';

export const appConfig = {
  providers: [
    provideRouter(routes, withComponentInputBinding())
  ]
};
```

2. Read parameters directly as inputs in the component:
```typescript
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-user-detail',
  template: `<p>User ID: {{ id }} | Search: {{ search }}</p>`
})
export class UserDetailComponent {
  @Input() id!: string;
  @Input() search?: string;
}
```

## Best Practices
1. **Use Functional Guards**: Modern routing logic ke liye legacy class-based guards ke badle lightweight functional guards (jaise `CanActivateFn`) use karein.
2. **Always Lazy Load Route Components**: Routes configurations me components ko directly import karne ke bajaye, bundle size small rakhne ke liye dynamic import function `loadComponent` ka use karein.
3. **Catch Wildcards**: Route configuration array ke end me wildcard `**` route configure karein taaki dynamic 404 views handle kiye ja sakein.

## Common Mistakes
* **Order of Routes**: Wildcard route (`**`) ko configuration array me sabse upar rakhna ek common mistake hai. Isse niche ke actual routes match nahi ho paate aur unexpected redirects hote hain.
* **Component Instantiation Errors**: Template me `<router-outlet></router-outlet>` directive lagana bhool jana, jiske bina matched route components display hi nahi honge.

## Interview Questions & Answers
### Q: What is lazy loading in routing and how is it implemented?
**A**: Lazy loading routing bundles ko demand ke according browser me load karne ki methodology hai. Ise implement karne ke liye `routes` definitions me components ko dynamic `loadComponent: () => import(...)` syntax se call kiya jata hai.

### Q: How do you read route parameters and query parameters in a component?
**A**: Route parameters ko dynamic query streams ya component params ke dynamic inputs se `ActivatedRoute` class ya `@Input` binding se clean format me resolve kar liya jata hai.

## Summary
Angular Router URLs aur component views ko map karta hai. Dynamic lazy loading ke zariye rendering performance clean hoti hai aur route guards routes ko secure banate hain.

---

Previous : [Services and Business Logic](./12_Services_and_Business_Logic.md) | Index : [Home](./00_index.md) | Next : [Template-Driven Forms](./14_Template_Driven_Forms.md)
