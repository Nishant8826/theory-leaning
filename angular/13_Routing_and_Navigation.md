# Routing and Navigation

## What is it?
Routing is the mechanism that maps URL paths in the browser to specific component views. It enables Single Page Applications (SPAs) to update views dynamically when a user navigates, without reloading the index page.

## Why do we need it?
Traditional websites request a new HTML document from the server for every link click, which slows down navigation. In an SPA, we download a single page, and the client-side router monitors URL changes (e.g. `/dashboard` to `/profile`), updating the DOM tree by swaping components instantly.

```
Routing Flow:
URL Change (/products/4) ──> Router evaluates path ──> Resolves lazy components
                          ──> Runs Guards (Auth check) ──> Loads data via Resolver
                          ──> Renders ProductDetailsComponent inside <router-outlet>
```

## How does it work?
1. **Route Definitions**: An array configuration mapping path strings to components.
2. **Router Outlet (`<router-outlet>`)**: A placeholder directive that acts as a container where matching components are dynamically loaded.
3. **Lazy Loading (`loadComponent`)**: Splits code into separate bundles, loading them only when a user navigates to those paths, keeping initial download size small.
4. **Guards (CanActivate, CanMatch)**: Functional gates that execute security checks (like authentication) before entering a route.
5. **Resolvers**: Pre-fetch API data before rendering components to prevent half-loaded layouts.

## Impact
* **Application Architecture**: Directs navigation boundaries, deep links, lazy-loading chunks, and access control.
* **Performance**: Lazy loading and pre-loading strategies significantly speed up initial page load.
* **Scalability**: Sub-routes and nested router outlets partition larger features into self-contained modules.

## Real World Example
In an online shopping application, navigating to `/admin` checks if the user has administrator privileges (via a guard). If the check passes, the application lazy-loads the admin dashboard bundle and renders it inside the router outlet.

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
Below is a complete implementation demonstrating child routes, lazy loading, parameters, and modern functional guards.

### `app.routes.ts`
```typescript
import { Routes, CanActivateFn } from '@angular/router';
import { inject } from '@angular/core';
import { Router } from '@angular/router';

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

### `admin-panel.component.ts` (Dynamic navigation parent)
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
        <!-- Route links with active styling classes -->
        <a routerLink="users" routerLinkActive="active-link">Manage Users</a> |
        <a routerLink="settings" routerLinkActive="active-link">Settings</a>
        <button (click)="logout()">Log Out</button>
      </nav>
      <main class="content">
        <!-- Sub components render dynamically here -->
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

## Best Practices
1. **Use Functional Guards**: Functional guards are preferred over legacy class-based guards in modern Angular as they reduce boilerplate.
2. **Always Lazy Load Route Components**: Avoid statically importing route components. Use `loadComponent` to generate individual javascript bundles.
3. **Catch Wildcards**: Always define a fallback route (`**`) at the bottom of your configuration array to catch invalid URLs.

## Common Mistakes
* **Order of Routes**: Putting wildcard routes (`**`) at the top of the route configuration. Since Angular matches routes sequentially, placing wildcards first will route all traffic to the fallback page.
* **Component Instantiation Errors**: Forgetting to add `<router-outlet></router-outlet>` in parent component templates, preventing child components from rendering.

## Interview Questions & Answers
### Q: What is lazy loading in routing and how is it implemented?
**A**: Lazy loading is an optimization technique that splits route components into separate javascript chunks and loads them only when the user navigates to those paths. It is implemented using `loadComponent` (or `loadChildren` for modules) with dynamic imports: `loadComponent: () => import('./path').then(m => m.Comp)`.

### Q: How do you read route parameters and query parameters in a component?
**A**: Inject `ActivatedRoute` and subscribe to `paramMap` or `queryParamMap` observables (or read inputs directly if `withComponentInputBinding()` is configured in the router bootstrap).

## Summary
The Angular Router maps browser paths to dynamic component templates. Using lazy loading (`loadComponent`), functional guards (`CanActivateFn`), and query parameters helps build secure, fast, and structured Single Page Applications.

---

Previous : [Services and Business Logic](./12_Services_and_Business_Logic.md) | Index : [Home](./00_index.md) | Next : [Template-Driven Forms](./14_Template_Driven_Forms.md)
