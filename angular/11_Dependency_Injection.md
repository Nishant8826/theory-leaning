# Dependency Injection

## What is it?
Dependency Injection (DI) is a design pattern where a class requests its dependencies from an external system rather than instantiating them itself. Angular has a built-in DI framework that handles class instantiation and lifecycle management, providing dependencies where requested.

## Why do we need it?
If components instantiate their own services (e.g. `const api = new ApiService()`), they become tightly coupled to those implementations. This makes testing difficult (you can't mock network requests), leads to duplicate instances, and limits flexibility. Angular's DI decouples classes, allowing you to swap mock implementations during testing or change providers globally without modifying component logic.

```
Without DI (Tightly Coupled):
Component ──> hardcoded "new ApiService()" ──> Hard to test, locked implementation

With DI (Decoupled):
Component requests "ApiService" ──> Angular DI Injector ──> Returns instance (can be mock or real)
```

## How does it work?
1. **Providers**: Instruct the DI system how to create dependency instances. Registered via `@Injectable()`, component decorators, or bootstrap configuration.
2. **Injector Hierarchy**: Angular uses a hierarchical injector tree:
   - **Platform Injector**: Configures platform-wide services.
   - **Root Injector**: Provides global singletons (`providedIn: 'root'`).
   - **Environment/Route Injector**: Instantiated for lazy-loaded route paths.
   - **Element Injector**: Dedicated to individual components and their template children.
3. **Lookup Resolution**: When a component requests a dependency, Angular checks its Element Injector. If not found, it traverses up the tree to the Root Injector. If the dependency isn't found anywhere, it throws a runtime error.

## Impact
* **Application Architecture**: Decouples services from components.
* **Performance**: Shared singletons save memory, and `providedIn: 'root'` services are tree-shakable.
* **Scalability**: Hierarchical injection allows sub-sections of an application (like feature routes) to manage their own isolated state.

## Real World Example
In a multi-tenant application, the UI requests an API client. The DI system determines the user's role and injects either the standard client or a premium client with caching capabilities without changing the component's code.

## Syntax
* **Inject via constructor**:
```typescript
constructor(private api: ApiService) {}
```
* **Inject via `inject()` function (modern)**:
```typescript
private api = inject(ApiService);
```
* **Injection Token**:
```typescript
export const API_URL = new InjectionToken<string>('ApiUrl');
```

## Hinglish Explanation

Dependency Injection (DI) ko simple terms me **"Catering Service"** ki tarah samajhein.
Agar aap ek class likh rahe hain, toh use chalne ke liye dusri classes (jaise API call helper, logging helper) ki zaroorat hoti hai. In dependencies ko class ke andar manually create karne ke bajaye (`const logger = new Logger()`), hum Angular se bolte hain: *"Bhai, mujhe Logger ka object laa kar de do!"* Aur Angular background me use create karke hume supply kar deta hai.

### 1. Dependency Inject Kaise Karte Hain? (Do Tarike)
* **Old Way (Constructor Injection):**
  ```typescript
  constructor(private apiService: ApiService) {}
  ```
* **New Way (`inject()` function):**
  ```typescript
  private apiService = inject(ApiService);
  ```
  Modern Angular me `inject()` function prefer kiya jata hai kyunki isse code simple aur readability behtar ho jati hai.

### 2. Injector Tree (Hierarchical Injector)
Angular me services ka ek hierarchy system hota hai:
* **Root Level (`providedIn: 'root'`):** Service poori application me singleton (poore app me sirf ek hi single copy) ban jati hai. Aur agar app me iska use kahi nahi ho raha, toh build time par yeh final bundle se remove (tree-shake) ho sakti hai.
* **Component Level (`providers: [MyService]`):** Agar kisi component ke `@Component` metadata ke `providers` array me service daal di, toh us component aur uske children ke liye ek bilkul naya, isolated instance banega.

### 3. Custom Providers (useClass, useValue, useFactory)
* **`useClass`:** Kisi class ke badle doosri replacement class use karna (jaise normal service ki jagah testing me MockService pass karna).
* **`useValue`:** Direct configuration static values ya configs inject karna.
* **`useFactory`:** Jab service object create karne ke liye hume dynamic checks ya complex factory code likhna pede.

## Code Examples
A comprehensive example showing Injection Tokens, Factory Providers, Multi Providers, and the `inject()` pattern:

```typescript
import { Component, Injectable, InjectionToken, inject } from '@angular/core';

// 1. Define Injection Token
export interface AppConfig {
  apiUrl: string;
  maxRetries: number;
}
export const APP_CONFIG = new InjectionToken<AppConfig>('ConfigToken');

// 2. Custom Injectable Service
@Injectable()
export class LoggerService {
  log(msg: string) {
    console.log(`[LOG]: ${msg}`);
  }
}

// 3. Conditional Service Provider (Factory)
@Injectable()
export class ApiService {
  constructor(
    private logger: LoggerService,
    private config: AppConfig
  ) {}

  fetchData() {
    this.logger.log(`Fetching from API: ${this.config.apiUrl}`);
  }
}

// 4. Demo Component demonstrating DI injection types
@Component({
  selector: 'app-di-demo',
  standalone: true,
  template: `
    <button (click)="load()">Fetch Data</button>
  `,
  providers: [
    // Element level injection
    LoggerService,
    {
      provide: APP_CONFIG,
      useValue: { apiUrl: 'https://api.my-app.com/v1', maxRetries: 3 }
    },
    {
      provide: ApiService,
      useFactory: () => {
        const logger = inject(LoggerService);
        const config = inject(APP_CONFIG);
        return new ApiService(logger, config);
      }
    }
  ]
})
export class DiDemoComponent {
  // Injecting using the modern inject() function
  private apiService = inject(ApiService);

  load() {
    this.apiService.fetchData();
  }
}
```

## Best Practices
1. **Prefer `providedIn: 'root'`**: Decorate services with `@Injectable({ providedIn: 'root' })` to make them global singletons and enable tree-shaking.
2. **Use the `inject()` Function**: Use the modern `inject()` function for property initialization to write cleaner classes and make inherits straightforward.
3. **Use Injection Tokens for Configurations**: Do not inject raw strings or arbitrary config objects directly. Use type-safe `InjectionToken` instances instead.

## Common Mistakes
* **Multiple Singleton instances**: Registering a service in a shared list of providers across components, which creates new service instances instead of utilizing the root singleton.
* **Injecting Services from a Lazy Module into Root**: Injecting a lazy-loaded service into a root-level component, which forces the lazy module to load during application startup and increases initial bundle sizes.

## Interview Questions & Answers
### Q: What is the difference between injecting a service via `providedIn: 'root'` and registering it in a component's `providers` array?
**A**: Declaring `providedIn: 'root'` registers the service as a global singleton. It is instantiated lazily on demand and can be tree-shaken if unused. Registering it in a component's `providers` array instantiates a new instance of the service dedicated to that component and its children, preventing it from being tree-shaken.
* **Hinglish Explanation**: `@Injectable({ providedIn: 'root' })` likhne se Angular us service ko ek global singleton (poori application me ek hi copy) bana deta hai, jo tabhi banti hai jab uski zaroorat ho aur tree-shaking support karti hai (agar service use nahi ho rahi toh final bundle se hat jati hai). Component ke `providers` array me register karne se us component aur uske bachon ke liye ek naya alag instance (copy) banta hai aur wo tree-shaken nahi ho pata.

### Q: What are multi-providers and what is a common use case for them?
**A**: Multi-providers allow you to register multiple dependencies under a single injection token by setting `multi: true`. A common use case is adding custom HTTP interceptors to Angular's built-in `HTTP_INTERCEPTORS` token.
* **Hinglish Explanation**: Multi-providers ka use ek single token ke under multiple dependencies ko register karne ke liye hota hai (`multi: true` set karke). Iska sabse common use-case `HTTP_INTERCEPTORS` me hota hai jahan hum ek hi HTTP token ke under multiple custom interceptors lines me add kar sakte hain.

## Summary
Dependency Injection decouples classes from their dependencies. Angular's hierarchical injector tree resolves dependencies at different levels, while custom providers (useClass, useValue, useFactory) and Injection Tokens customize how instances are created.

---

Previous : [Signals](./10_Signals.md) | Index : [Home](./00_index.md) | Next : [Services and Business Logic](./12_Services_and_Business_Logic.md)
