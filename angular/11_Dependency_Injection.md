# Dependency Injection

## What is it?
Dependency Injection (DI) is a core software design pattern in which a class receives its required dependencies from an external source rather than instantiating them itself. Angular includes a powerful, built-in hierarchical Dependency Injection framework that automatically creates, manages, and injects class dependencies wherever they are needed across the application.

## Why do we need it?
If components manually instantiate their own dependencies (e.g., `const api = new ApiService()`), components become tightly coupled to concrete implementations. This makes automated unit testing nearly impossible (you cannot swap network calls for mock services), leads to duplicate object instances, and produces rigid, fragile code. 

Angular's DI system decouples components from concrete service implementations, making code modular, reusable, easily configurable, and highly testable.

```
Without Dependency Injection (Tightly Coupled):
Component ──> Hardcoded "new ApiService()" ──> Hard to test, locked implementation

With Dependency Injection (Decoupled & Testable):
Component requests "ApiService" ──> Angular DI Injector ──> Injects singleton/mock instance
```

## How does it work?
1. **Providers**: Tell the DI system how to construct an injectable dependency. Providers can be configured via `@Injectable({ providedIn: 'root' })`, inside `ApplicationConfig` (`app.config.ts`), inside route configuration files (`app.routes.ts`), or within a component's `providers: [...]` metadata array.
2. **Injector Hierarchy**: Angular organizes injectors into a hierarchical tree:
   - **Platform Injector**: Configures platform-specific singletons.
   - **Root Injector**: Provides application-wide, tree-shakable singletons (`providedIn: 'root'`).
   - **Environment/Route Injector**: Provides scoped services for lazy-loaded route branches.
   - **Element Injector**: Scoped specifically to a parent component and its child component views.
3. **Resolution Lookup**: When a component requests a dependency, Angular first searches the local Element Injector. If not found, it bubbles up the injector hierarchy to the Route Injector, and finally to the Root Injector. If the dependency cannot be resolved anywhere, Angular throws a `NullInjectorError`.

## Impact
* **Application Architecture**: Strictly decouples UI view components from data processing, storage, and networking layers.
* **Performance**: Shared singletons prevent redundant object allocations, and `providedIn: 'root'` enables optimal tree-shaking (unused services are excluded from production bundles).
* **Scalability**: Hierarchical scoping allows feature modules to maintain private, isolated state without polluting the global application context.

## Real World Example
In a multi-tenant enterprise portal, a UI component requests an abstract `DataService`. Based on whether the active user is an enterprise customer or a standard user, the DI factory injects either `EnterpriseDataService` or `StandardDataService` dynamically without modifying a single line of component code.

## Syntax
* **Constructor Injection**:
```typescript
constructor(private api: ApiService) {}
```
* **Modern `inject()` Function**:
```typescript
private api = inject(ApiService);
```
* **Custom Injection Token**:
```typescript
export const API_URL = new InjectionToken<string>('ApiUrl');
```

## Code Examples
Below is a complete implementation demonstrating Injection Tokens, Factory Providers, and the modern `inject()` pattern:

```typescript
import { Component, Injectable, InjectionToken, inject } from '@angular/core';

// 1. Define an Injection Token for application configuration
export interface AppConfig {
  apiUrl: string;
  maxRetries: number;
}
export const APP_CONFIG = new InjectionToken<AppConfig>('ConfigToken');

// 2. Injectable Logger Service
@Injectable()
export class LoggerService {
  log(message: string): void {
    console.log(`[LOGGER]: ${message}`);
  }
}

// 3. Service consuming another service and configuration token
@Injectable()
export class ApiService {
  constructor(
    private logger: LoggerService,
    private config: AppConfig
  ) {}

  fetchData(): void {
    this.logger.log(`Fetching resources from API endpoint: ${this.config.apiUrl}`);
  }
}

// 4. Demo Component configuring and injecting providers
@Component({
  selector: 'app-di-demo',
  standalone: true,
  template: `
    <div class="demo-box">
      <h3>Dependency Injection Demo</h3>
      <button (click)="load()">Fetch API Data</button>
    </div>
  `,
  providers: [
    LoggerService,
    {
      provide: APP_CONFIG,
      useValue: { apiUrl: 'https://api.enterprise-app.com/v1', maxRetries: 3 }
    },
    {
      provide: ApiService,
      useFactory: () => {
        const logger = inject(LoggerService);
        const config = inject(APP_CONFIG);
        return new ApiService(logger, config);
      }
    }
  ],
  styles: [`
    .demo-box { padding: 16px; border: 1px solid #6366f1; border-radius: 8px; max-width: 320px; }
    button { padding: 8px 16px; background: #6366f1; color: white; border: none; border-radius: 4px; cursor: pointer; }
  `]
})
export class DiDemoComponent {
  // Modern injection using inject()
  private apiService = inject(ApiService);

  load(): void {
    this.apiService.fetchData();
  }
}
```

## Best Practices
1. **Always Prefer `providedIn: 'root'`**: Decorate general services with `@Injectable({ providedIn: 'root' })`. This guarantees a single application-wide instance and enables tree-shaking if the service is unused.
2. **Use the `inject()` Function**: Prefer the modern `inject()` function over constructor injection for cleaner class declarations, simpler inheritance, and composable functional utilities.
3. **Use `InjectionToken` for Configuration Objects and Primitives**: When injecting primitive values, third-party libraries, or configuration objects, always create a typed `InjectionToken` instead of injecting raw strings or untyped objects.

## Common Mistakes
* **Duplicate Service Instances**: Unintentionally adding a singleton service to a component's `providers: [...]` array creates a brand-new instance for that component and its children, breaking shared singleton state.
* **Injecting Lazy-Loaded Services into Root**: Attempting to inject a service scoped to a lazy-loaded route into a root component breaks code-splitting and causes injection resolution errors.

## Interview Questions & Answers
### Q: What is the difference between `providedIn: 'root'` and listing a service in a component's `providers` array?
**A**: `providedIn: 'root'` registers the service with the root injector, making it a tree-shakable singleton accessible anywhere in the application. Listing a service in a component's `providers` array creates a new, isolated instance tied to that specific component's lifecycle and its child tree, preventing tree-shaking.

### Q: What are Multi-Providers and where are they commonly used in Angular?
**A**: Multi-providers allow multiple provider definitions to be bound to a single injection token (`multi: true`). When injected, Angular provides an array containing all registered instances. The most prominent use case is registering multiple HTTP interceptors using `HTTP_INTERCEPTORS`.

## Summary
Dependency Injection decouples application layers, promotes reusability, and makes automated testing straightforward. Angular's hierarchical injector tree, rich provider recipes (`useClass`, `useValue`, `useFactory`), and custom `InjectionToken` APIs give developers complete control over dependency resolution.

---

Previous : [Signals](./10_Signals.md) | Index : [Home](./00_index.md) | Next : [Services and Business Logic](./12_Services_and_Business_Logic.md)
