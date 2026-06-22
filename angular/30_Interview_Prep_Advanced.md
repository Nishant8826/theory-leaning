# Advanced Interview Prep

## What is it?
Advanced Interview Preparation compiles complex concepts, performance optimization rules, and design choices that developers should know when interviewing for senior-level Angular roles.

## Why do we need it?
Senior roles require a deep understanding of runtime performance, state synchronization, server-side rendering, and advanced RxJS streams. Reviewing topics like change detection customization, custom dependency injectors, silent token refreshes, and rendering engine architectures prepares candidates for advanced system design discussions.

```
Preparation Flow:
Review Change Detection (OnPush) ──> Study DI Injection Tree ──> Practice RxJS Flattening ──> Learn SSR/Hydration ──> Master System Design
```

## How does it work?
1. **Performance Tuning**: Covers OnPush change detection, Zoneless execution, and lazy-loaded structures.
2. **Advanced DI**: Tests knowledge of multi-providers, hierarchical injectors, and factory configurations.
3. **Async Coordination**: Verifies familiarity with flattening operators, silent refreshes, and state stores.

## Impact
* **Application Architecture**: Directs how decoupled, testable, and secure enterprise architectures are built.
* **Performance**: Promotes strategies to minimize initial load times and keep rendering smooth.
* **Scalability**: Helps developers structure applications that can be split into micro-frontends or monorepos.

## Real World Example
A candidate is asked how to configure a component to render without Zone.js. The candidate explains how to leverage Angular's Signals API and configure Zoneless change detection in the bootstrap providers, demonstrating senior-level knowledge of performance optimization.

## Syntax
A custom factory provider with dependencies:
```typescript
{
  provide: MyService,
  useFactory: () => {
    const http = inject(HttpClient);
    return new MyService(http);
  }
}
```

## Hinglish Explanation

Advanced / Senior level developer roles me application design, custom architecture layers, performance metrics, SSR rendering flow aur complex DI structures par conceptual questions pooche jate hain:

### 1. experimental Zoneless mode (Performance)
* Zone.js browser runtime ke basic actions (click, async events) ko override karke dirty check scan chalata hai. Modern Angular me `provideExperimentalZonelessChangeDetection()` call karke Zone.js remove kar diya jata hai, jisse reactivity strictly Signals par depend ho jati hai aur render speed drastically build ho jati hai.

### 2. Dependency Injection Tree Resolution
* Angular DI system hierarchical format me classes dependencies resolve karta hai. Sabse pehle local Component Injector scan hota hai, phir nested steps ke through parents, dynamic route injection configs, root injector aur platform configurations tak sequence checking chalti hai jab tak token active provider reference match na kare.

### 3. Hydration details (SSR discrepancies)
* Server rendering me generated static layout aur client browser JavaScript execute ho kar build hone wale runtime layout hierarchy identical hone chahiye. Agar dynamic layout changes browser platform checks lagaye bina local references modify karein, toh client browser rendering me mismatch logs validation warnings aayengi.

## Code Examples
Below is an implementation of a custom injection token and dynamic factory provider that resolves different service instances based on configuration variables.

```typescript
import { InjectionToken, inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

export interface StorageConfig {
  driver: 'local' | 'cloud';
}

export const STORAGE_CONFIG = new InjectionToken<StorageConfig>('StorageConfig');

@Injectable()
export abstract class StorageService {
  abstract save(data: string): void;
}

@Injectable()
export class LocalStorageService extends StorageService {
  save(data: string): void {
    localStorage.setItem('data', data);
  }
}

@Injectable()
export class CloudStorageService extends StorageService {
  private http = inject(HttpClient);
  save(data: string): void {
    this.http.post('https://api.my-app.com/save', { data }).subscribe();
  }
}

// Factory provider function
export const storageProvider = {
  provide: StorageService,
  useFactory: () => {
    const config = inject(STORAGE_CONFIG);
    return config.driver === 'cloud' 
      ? new CloudStorageService() 
      : new LocalStorageService();
  }
};
```

## Best Practices
1. **Default to OnPush**: Configure `ChangeDetectionStrategy.OnPush` on all components to limit change detection checks.
2. **Use `CanMatch` to Secure Chunks**: Secure routes using `CanMatch` functional guards to prevent unauthorized users from downloading restricted code bundles.
3. **Wrap browser-specific code in checks**: Wrap all references to browser-specific globals (like `window` or `document`) in platform checks to ensure SSR compatibility.

## Common Mistakes
* **Mutating references inside OnPush components**: Mutating object properties directly in components that use the `OnPush` strategy, which prevents Angular from detecting changes.
* **Creating memory leaks in HTTP interceptors**: Forgetting to clean up mock HTTP testing configurations or creating infinite redirect loops during silent token refreshes.

## Interview Questions & Answers

### Q1: How does `ChangeDetectionStrategy.OnPush` work and when should it be used?
**A**: `OnPush` change detection instructs Angular to skip checking a component and its children unless it receives updated input references, event handlers trigger within the component, or you request a check manually using `ChangeDetectorRef`. It should be configured by default on all components to optimize change detection performance.
* **Hinglish Explanation**: `OnPush` strategy me Angular component aur uske children ko change detection scan se skip kar deta hai. Yeh sirf tabhi check karta hai jab: (1) Component ko parent se naya `@Input()` reference mile, (2) Component template me koi event trigger ho, ya (3) Hum manually `ChangeDetectorRef` ke zariye request karein. Performance optimize karne ke liye senior developers ise by default use karte hain.

### Q2: What is Zoneless Angular and how is it implemented?
**A**: Zoneless Angular removes Zone.js dependency, relying on Signals to trigger DOM updates directly. This reduces change detection checks and initial bundle sizes. It is implemented by removing `zone.js` imports and registering `provideExperimentalZonelessChangeDetection()` during bootstrapping.
* **Hinglish Explanation**: Zoneless Angular me Zone.js library ko completely bypass kiya jata hai. Isme reactivity ke liye completely Angular Signals API ka use hota hai. Ise implement karne ke liye `zone.js` imports ko remove karte hain aur app bootstrap ke providers array me `provideExperimentalZonelessChangeDetection()` function register karte hain. Isse bundle size bohot drop ho jata hai.

### Q3: Explain how the hierarchical Dependency Injection tree works.
**A**: Angular's DI system uses a tree structure to resolve dependencies, starting from the Element Injector where the request originated, and traversing up through Route, Root, and Platform injectors until it resolves the token or throws a runtime error.
* **Hinglish Explanation**: Angular me DI tree elements, modules, aur routes ke nested hierarchy system par resolve hota hai. Jab koi component kisi service ka demand token fetch karta hai, ko Angular sabse pehle local Component Injector me check karta hai. Agar wahan na mile, toh upward direction me navigation guards, modules, App root, aur ant me framework platform injectors par traverse karta hai jab tak token resolve na ho jaye.

### Q4: Explain the differences between the RxJS flattening operators: `switchMap`, `mergeMap`, `concatMap`, and `exhaustMap`.
**A**:
- `switchMap`: Cancels the active inner observable when a new value arrives (ideal for live searches).
- `mergeMap`: Processes all inner observables concurrently (ideal for parallel operations).
- `concatMap`: Queues inner observables to run sequentially in order (ideal for transactional updates).
- `exhaustMap`: Ignores new emissions while the current inner observable is running (ideal for preventing double clicks on submit buttons).
* **Hinglish Explanation**: 
  - `switchMap`: New request aane par active network request cancel kar deta hai (live search options ke liye best).
  - `mergeMap`: Parallel requests run karta hai bina kisi request cancel kiye (chat inputs).
  - `concatMap`: Queue system me serial updates data stream check karta hai (transactions).
  - `exhaustMap`: Current request running status me duplicate clicks (double-clicks submit actions) ignore karta hai.

### Q5: How do you handle authentication silent refreshes inside an HTTP Interceptor?
**A**: When an API request fails with a `401 Unauthorized` status, the interceptor catches the error, calls an auth service to request a new access token using a refresh token, updates storage, and retries the original request with the new access token. If the refresh request fails, it redirects the user to `/login`.
* **Hinglish Explanation**: HTTP Interceptor outgoing requests me data validation verify karta hai. Jab API 401 error throw karti hai (token expire), interceptor request ko intercept karke `refreshToken` service call karta hai. Agar refresh logic se new access token generate ho jata hai, toh request update headers ke sath retry ho jati hai, warna user redirect login route par force close ho jata hai.

### Q6: What are hydration errors in SSR and how can you resolve them?
**A**: Hydration errors occur when the DOM structure pre-rendered on the server does not match the DOM structure built by the client-side JavaScript. They can be resolved by avoiding manual DOM mutations, checking platform types before accessing browser-only globals, and using `provideClientHydration()`.
* **Hinglish Explanation**: Hydration errors tab aate hain jab server-rendered HTML aur client-compiled JS DOM structure me content discrepancy (difference) ho. Ise solve karne ke liye manual DOM mutations bypass check bypass methods use karein, platform checks implement karein aur root bootstrap me `provideClientHydration()` load karein.

## Summary
Advanced interviews focus on runtime optimizations, custom dependency injection configurations, and server-side rendering support. Reviewing these topics helps senior candidates demonstrate their system design capabilities.

---

Previous : [Intermediate Interview Prep](./29_Interview_Prep_Intermediate.md) | Index : [Home](./00_index.md) | Next : [Scenario and System Design](./31_Interview_Prep_Scenario_and_System_Design.md)
