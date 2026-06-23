# Dependency Injection

## What is it?
Dependency Injection (DI) ek software design pattern hai jahan ek class apni dependencies ko khud create (instantiate) karne ke bajaye kisi external system se demand karti hai. Angular ke paas ek built-in DI framework hota hai jo classes instantiation aur lifecycle management ko internally process karta hai, aur jahan bhi zaroorat ho dependencies supply karta hai.

## Why do we need it?
Agar components apni services khud hi instantiate karne lagenge (jaise `const api = new ApiService()`), toh components aur services aapas me tightly coupled ho jayenge. Isse unit testing mushkil ho jayegi (aap network requests ko mock nahi kar payenge), duplicate instances banenge, aur structure strict ho jayega. Angular ka DI design is dependency coupling ko dur karta hai, jisse unit tests me mock classes pass karna aur global configurations update karna aasan ho jata hai.

```
Without DI (Tightly Coupled):
Component ──> hardcoded "new ApiService()" ──> Hard to test, locked implementation

With DI (Decoupled):
Component requests "ApiService" ──> Angular DI Injector ──> Returns instance (can be mock or real)
```

## How does it work?
1. **Providers**: DI system ko instructions dete hain ki kisi dependency ka object kaise create karna hai. Inhe `@Injectable()`, component decorators metadata, ya `app.routes.ts` environment options me configure kiya jata hai.
2. **Injector Hierarchy**: Angular hierarchical injector tree use karta hai:
   - **Platform Injector**: Platform level features coordinate karta hai.
   - **Root Injector**: Global singletons compile karta hai (`providedIn: 'root'`).
   - **Environment/Route Injector**: Lazy-loaded routes ke path par elements create karta hai.
   - **Element Injector**: Specific parent components aur unke child views levels par inject hota hai.
3. **Lookup Resolution**: Jab koi component dependency ki request karta hai, Angular pehle local Element Injector check karta hai. Agar wahan nahi milta, toh hierarchical path se Root Injector tak up direction me search parameters check karta hai. Agar match nahi milta, toh compiler/runtime exception alert call hoti hai.

## Impact
* **Application Architecture**: UI presentation aur logic data layer ke beech binding details fully decouple rakhta hai.
* **Performance**: Shared singletons memory waste control karte hain aur `providedIn: 'root'` configurations tree-shakable bundles download optimize karti hain.
* **Scalability**: Hierarchical tree layout projects feature packages ko unki local routing boundary me secure state manage karne ki features deta hai.

## Real World Example
Ek multi-tenant enterprise portal me, UI component API data loading request karta hai. DI system authentication status check karke decide karta hai ki user premium hai ya normal aur dynamic coordinates check karke appropriate PremiumClient ya StandardClient data injector inject kar deta hai bina component code lines modify kiye.

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

## Code Examples
Neeche Injection Tokens, Factory Providers, Multi Providers, aur `inject()` pattern ka complete design integration example diya gaya hai:

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
  private apiService = inject(ApiService);

  load() {
    this.apiService.fetchData();
  }
}
```

## Best Practices
1. **Prefer `providedIn: 'root'`**: Services ko `@Injectable({ providedIn: 'root' })` decorator se setup karein taaki wo global singletons rahein aur unused components compile build se automatically remove (tree-shake) ho sakein.
2. **Use the `inject()` Function**: Property setup declarations me clean typescript structure maintenance aur linear layouts class inheritance ke liye modern `inject()` use karein.
3. **Use Injection Tokens for Configurations**: Config values or constants pass karne ke liye simple object maps/strings target na karein. Type-safe custom `InjectionToken` use karein.

## Common Mistakes
* **Multiple Singleton instances**: Shared services list ko multiple sub-components level `providers` metadata arrays me add karna, jo single root resource ke bajaye har component level par dynamic unique copies create kar deta hai.
* **Injecting Services from a Lazy Module into Root**: Lazy route module service parameters ko direct root level main component me inject karna, jo application loading startup behavior scale aur page initial rendering slow kar deta hai.

## Interview Questions & Answers
### Q: What is the difference between injecting a service via `providedIn: 'root'` and registering it in a component's `providers` array?
**A**: `providedIn: 'root'` service ko global singleton aur tree-shakable banata hai. Component level providers array use karne se specific component aur child levels ke liye unique isolated objects generate hote hain aur tree-shaking prevent hoti hai.

### Q: What are multi-providers and what is a common use case for them?
**A**: Multi-providers multiple class bindings ko single array collection token me bundle karte hain (`multi: true` property ke zariye). HTTP interceptors stack pipeline design iska best utility example hai.

## Summary
Dependency Injection service modules dependency decoupling manage karta hai. Angular hierarchy structures options customizable setups (useClass, useValue, useFactory) aur custom Injection Tokens developers ko clean objects injection controls create karne me leverage karte hain.

---

Previous : [Signals](./10_Signals.md) | Index : [Home](./00_index.md) | Next : [Services and Business Logic](./12_Services_and_Business_Logic.md)
