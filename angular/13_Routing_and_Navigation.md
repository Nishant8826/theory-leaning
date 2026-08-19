# Routing and Navigation

## What is it?
Routing in Angular is the mechanism that maps browser URL paths to specific components. It enables Single Page Applications (SPAs) to display different views dynamically as the user navigates, without performing a full-page browser reload.

## Why do we need it?
In traditional multi-page web applications, clicking a link causes the browser to request an entirely new HTML document from the server, resulting in slow page reloads and a jarring user experience. 

Angular Router transforms the application into an SPA by loading a single HTML shell and dynamically swapping view components in and out of designated placeholders based on URL changes.

```
Routing Flow:
URL Change (/products/42) ──> Router evaluates route definitions 
                          ──> Checks Route Guards (Auth / Role check) 
                          ──> Downloads Lazy-Loaded Component Chunk
                          ──> Resolves Route Data (Resolvers)
                          ──> Renders ProductDetailsComponent inside <router-outlet>
```

## How does it work?
1. **Route Configuration**: An array of `Route` objects mapping URL paths to components or lazy-loaded modules.
2. **Router Outlet (`<router-outlet>`)**: A dynamic placeholder directive where Angular inserts the component matched by the active route.
3. **Lazy Loading (`loadComponent` / `loadChildren`)**: Splits the application bundle into smaller feature chunks that are downloaded on demand only when the user navigates to that route.
4. **Route Guards (`CanActivateFn`, `CanMatchFn`, `CanDeactivateFn`)**: Functional security checkpoints that allow or block route access based on conditions like authentication or unsaved form changes.
5. **Resolvers**: Pre-fetch necessary backend data before the target route component finishes activating and rendering.

## Impact
* **Application Architecture**: Provides a clean, hierarchical structure for navigation, child routes, and application layout sections.
* **Performance**: Lazy loading drastically reduces the initial JavaScript bundle size, speeding up Time-to-Interactive (TTI).
* **Scalability**: Nested child routes allow complex dashboards with independent sub-views to scale cleanly across multiple development teams.

## Real World Example
In an enterprise e-commerce platform, when an administrator navigates to `/admin/orders`:
1. The `authGuard` checks for a valid session and admin role.
2. The router dynamically downloads the lazy-loaded `AdminOrdersComponent` chunk.
3. The layout displays the administration sidebar and renders order data inside the `<router-outlet>`.

## Syntax
* **Lazy Route Configuration**:
```typescript
{ 
  path: 'products/:id', 
  loadComponent: () => import('./detail.component').then(m => m.DetailComponent) 
}
```
* **Declarative Template Navigation (`routerLink`)**:
```html
<a routerLink="/products/12" [queryParams]="{ ref: 'email' }">View Product</a>
```
* **Programmatic Navigation (`Router.navigate`)**:
```typescript
this.router.navigate(['/products', 12], { queryParams: { ref: 'email' } });
```

## Code Examples
Below is a complete implementation featuring child routes, lazy loading, route parameters, and modern functional guards:

### `app.routes.ts`
```typescript
import { Routes, Router, CanActivateFn } from '@angular/router';
import { inject } from '@angular/core';

// 1. Define a Modern Functional Route Guard
export const authGuard: CanActivateFn = () => {
  const router = inject(Router);
  const isLoggedIn = !!localStorage.getItem('auth_token'); // Authentication check

  return isLoggedIn ? true : router.createUrlTree(['/login']);
};

// 2. Application Route Definitions
export const routes: Routes = [
  { 
    path: 'login', 
    loadComponent: () => import('./login.component').then(m => m.LoginComponent) 
  },
  {
    path: 'admin',
    canActivate: [authGuard],
    // Lazy load the parent feature component
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
  { 
    path: '**', 
    loadComponent: () => import('./not-found.component').then(m => m.NotFoundComponent) 
  }
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
        <a routerLink="users" routerLinkActive="active-link">Manage Users</a>
        <a routerLink="settings" routerLinkActive="active-link">Settings</a>
        <button (click)="logout()">Log Out</button>
      </nav>
      <main class="content">
        <!-- Child routes render here -->
        <router-outlet></router-outlet>
      </main>
    </div>
  `,
  styles: [`
    .admin-layout { display: flex; min-height: 80vh; font-family: sans-serif; }
    .sidebar { width: 220px; padding: 20px; background: #f3f4f6; display: flex; flex-direction: column; gap: 10px; }
    .active-link { font-weight: bold; color: #2563eb; }
    .content { flex: 1; padding: 20px; }
    button { margin-top: auto; padding: 8px; cursor: pointer; }
  `]
})
export class AdminPanelComponent {
  private router = inject(Router);

  logout(): void {
    localStorage.removeItem('auth_token');
    this.router.navigate(['/login']);
  }
}
```

### Reading Route Parameters and Query Parameters

#### Approach 1: Modern Component Input Binding (Angular 16+)

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

2. Read path parameters and query parameters directly as `@Input()` properties:
```typescript
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-user-detail',
  standalone: true,
  template: `
    <div class="user-card">
      <p>User ID (from path param): {{ id }}</p>
      <p>Filter Search (from query param): {{ search }}</p>
    </div>
  `
})
export class UserDetailComponent {
  @Input() id!: string;         // Automatically populated from /users/:id
  @Input() search?: string;     // Automatically populated from ?search=...
}
```

#### Approach 2: Traditional `ActivatedRoute` Observable Streams
```typescript
import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-user-detail-stream',
  standalone: true,
  template: `<p>User ID: {{ userId }} | Search: {{ searchVal }}</p>`
})
export class UserDetailStreamComponent implements OnInit {
  private route = inject(ActivatedRoute);
  userId: string | null = null;
  searchVal: string | null = null;

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.userId = params.get('id');
    });

    this.route.queryParamMap.subscribe(params => {
      this.searchVal = params.get('search');
    });
  }
}
```

## Best Practices
1. **Use Modern Functional Guards**: Prefer `CanActivateFn` and `CanMatchFn` over deprecated class-based guards. Functional guards are cleaner, easier to compose, and can use `inject()` directly.
2. **Lazy Load All Feature Routes**: Always use `loadComponent: () => import(...)` for feature views to ensure initial application bundles remain lightweight.
3. **Always Add a Wildcard Route**: Place `{ path: '**', ... }` at the very end of your routes array to handle unmatched URLs and render a 404 page gracefully.
4. **Use `withComponentInputBinding()`**: Simplify parameter extraction by binding route and query parameters directly to component inputs instead of manually subscribing to `ActivatedRoute`.

## Common Mistakes
* **Incorrect Route Ordering**: Placing the wildcard route (`**`) at the beginning or middle of the `routes` array. Because Angular evaluates routes top-to-bottom using a first-match-wins strategy, placing `**` too early prevents subsequent valid routes from ever matching.
* **Missing `<router-outlet>`**: Forgetting to add `<router-outlet></router-outlet>` in the parent component template. Without the outlet placeholder, matched child components will not be rendered.

## Interview Questions & Answers
### Q: What is lazy loading in Angular routing and how is it configured?
**A**: Lazy loading is an optimization technique that splits route components into separate JavaScript chunks loaded asynchronously only when the user navigates to that specific path. In modern standalone Angular, it is configured in the routes definition using the `loadComponent` (for a single component) or `loadChildren` (for child route trees) syntax with dynamic `import()`.

### Q: How do Functional Route Guards work in Angular?
**A**: Functional route guards (like `CanActivateFn`) are standalone functions executed by the router before navigating to a route. They can return a `boolean`, `UrlTree` (for redirection), or an `Observable`/`Promise` of either. They leverage Angular's `inject()` function to resolve dependencies like `AuthService` and `Router` directly without requiring class boilerplate.

## Summary
Angular Router maps URL paths to component views, managing navigation in Single Page Applications. Modern routing features standalone lazy loading, functional guards for access control, nested child routes, and component input binding for effortless parameter resolution.

---

Previous : [Services and Business Logic](./12_Services_and_Business_Logic.md) | Index : [Home](./00_index.md) | Next : [Template-Driven Forms](./14_Template_Driven_Forms.md)
