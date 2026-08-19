# Angular Architecture

## What is it?
Angular Architecture is the foundational blueprint of the framework. It defines how visual views (HTML Templates), styling (CSS/SCSS), component logic (TypeScript classes), dependency injectors, and data providers (Services) interact, compile, and coordinate to power a robust Single Page Application (SPA).

## Why do we need it?
Without a structured architectural pattern, software complexity increases rapidly as codebases grow. Developers might embed business logic directly into HTML templates, create redundant HTTP requests, or build fragile component communication chains. Angular's architecture enforces a strict **Separation of Concerns**, ensuring that every class has a single, well-defined responsibility (Presentation, Structure, Behavior, State, or Backend Integration).

```
┌────────────────────────────────────────────────────────┐
│                      Angular App                       │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
          ┌──────────────────────────────────┐
          │  bootstrapApplication(AppComponent)│
          └────────────────┬─────────────────┘
                           │
                           ▼
              ┌────────────────────────────┐
              │       Root Component       │
              │       (AppComponent)       │
              └─────────────┬──────────────┘
                            │
                            ▼
              ┌────────────────────────────┐
              │    Sub-Components Tree     │
              │  (Home, Products, Login)   │
              └─────────────┬──────────────┘
                            │
                            ▼
              ┌────────────────────────────┐
              │  Shared Services / APIs    │
              │  (Dependency Injection)    │
              └────────────────────────────┘
```

## How does it work?
1. **Bootstrapping**: When the application loads in the browser, `index.html` loads and `main.ts` executes. In modern Angular, `bootstrapApplication(AppComponent, appConfig)` initializes the application and renders the primary root component into the DOM.
2. **Standalone Components**: The fundamental building blocks of modern Angular. They declare their own dependencies directly in their component metadata (`imports: [...]`), eliminating the need for intermediary `NgModule` definitions.
3. **Dependency Injection (DI)**: A hierarchical injection engine that provides services to components. When a component declares a service dependency, Angular's DI system resolves or instantiates the service instance, maintaining clear isolation between UI rendering and business logic.

## Impact
* **Application Architecture**: Creates a predictable component tree where UI elements communicate via structured inputs, outputs, and shared data services.
* **Performance**: Standalone components enable precise code-splitting and deep tree-shaking, resulting in smaller initial bundle sizes and faster load times.
* **Scalability**: Hierarchical dependency injection allows feature branches and lazy-loaded routes to encapsulate their own private state and services cleanly.

## Real World Example
In an enterprise banking dashboard, visual interface elements (transaction tables, balance cards, navigation menus) are individual reusable components. Meanwhile, authentication state, API communication, and financial balance calculations reside in dedicated services injected where needed.

## Syntax
Modern Angular applications configure global providers using `ApplicationConfig` in `app.config.ts`:

```typescript
import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideHttpClient()
  ]
};
```

## Code Examples
Below is a complete implementation of a modern standalone application structure:

### `main.ts`
```typescript
import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error('Application bootstrap error:', err));
```

### `app/app.component.ts`
```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  template: `
    <header class="app-header">
      <h1>Enterprise Angular Dashboard</h1>
    </header>
    <main>
      <p>Bootstrap status: Application Initialized Successfully</p>
    </main>
  `,
  styles: [`
    .app-header { 
      background: #1f2937; 
      color: white; 
      padding: 15px; 
      text-align: center; 
    }
    main { 
      padding: 20px; 
      text-align: center; 
      font-family: sans-serif; 
    }
  `]
})
export class AppComponent {}
```

## Best Practices
1. **Always Use Standalone Architecture**: Avoid creating new `NgModule` files. Set `standalone: true` for all new components, directives, and pipes.
2. **Centralize Global Providers in `app.config.ts`**: Register global application infrastructure (Router, HttpClient, NgRx Store, Interceptors) within `appConfig` during bootstrap.
3. **Decouple View from Business Logic**: Never write heavy mathematical calculations, direct HTTP calls, or localStorage manipulation inside component classes. Delegate these tasks to injectable services.

## Common Mistakes
* **Bootstrapping Multiple Root Components**: Trying to bootstrap multiple sibling components in `index.html`. Always bootstrap a single root component (`AppComponent`) and render additional components through template nesting and routing.
* **Circular Dependencies**: Importing Component A into Component B while also importing Component B into Component A. Structure component hierarchies strictly top-down, or use a shared service to coordinate interactions.

## Interview Questions & Answers
### Q: What is bootstrapping in Angular, and how has it evolved in modern versions?
**A**: Bootstrapping is the process by which Angular initializes its runtime, compiles the root component, and inserts it into the browser's DOM (`index.html`). In legacy Angular versions, this required an `NgModule` (`platformBrowserDynamic().bootstrapModule(AppModule)`). Modern Angular uses the lightweight, standalone API `bootstrapApplication(AppComponent, appConfig)`, reducing boilerplate and improving build performance.

### Q: What are Standalone Components and what problems do they solve?
**A**: Standalone components are self-contained Angular components that do not require an intermediary `NgModule` container. They declare their required dependencies directly in their `imports` array. This eliminates module configuration overhead, makes components easily reusable across projects, and optimizes tree-shaking for smaller production bundles.

## Summary
Modern Angular architecture is built around Standalone components and centralized application configurations. This setup leverages TypeScript and hierarchical Dependency Injection to ensure a clean separation between presentation views, application routing, and business logic.

---

Previous : [TypeScript Fundamentals](./03_Typescript_Fundamentals.md) | Index : [Home](./00_index.md) | Next : [Components and Templates](./05_Components_and_Templates.md)
