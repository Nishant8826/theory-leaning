# Advanced Interview Prep

## What is it?
Advanced Interview Preparation un complex concepts, performance optimization rules, aur design choices ka compilation hai jo developers ko senior-level Angular roles ke liye interview dete waqt pata hone chahiye.

## Why do we need it?
Senior roles ke liye runtime performance, state synchronization, server-side rendering, aur advanced RxJS streams ki deep understanding hona zaroori hai. Change detection customization, custom dependency injectors, silent token refreshes, aur rendering engine architectures jaise topics ko review karne se candidates advanced system design discussions ke liye prepare ho jate hain.

```
Preparation Flow:
Review Change Detection (OnPush) ──> Study DI Injection Tree ──> Practice RxJS Flattening ──> Learn SSR/Hydration ──> Master System Design
```

## How does it work?
1. **Performance Tuning**: OnPush change detection, Zoneless execution, aur lazy-loaded structures ko cover karta hai.
2. **Advanced DI**: Multi-providers, hierarchical injectors, aur factory configurations ki knowledge ko test karta hai.
3. **Async Coordination**: Flattening operators, silent refreshes, aur state stores ke familiarity ko verify karta hai.

## Impact
* **Application Architecture**: Decoupled, testable, aur secure enterprise architectures kaise build kiye jayein, use direct karta hai.
* **Performance**: Initial load times ko minimize karne aur rendering ko smooth rakhne wali strategies ko promote karta hai.
* **Scalability**: Developers ko aisi applications structure karne me help karta hai jinhe micro-frontends ya monorepos me split kiya ja sake.

## Real World Example
Ek candidate se pucha jata hai ki Zone.js ke bina render karne ke liye component ko kaise configure karein. Candidate explain karta hai ki Angular ke Signals API ka leverage kaise karein aur bootstrap providers me Zoneless change detection ko kaise configure karein, jo performance optimization ke senior-level knowledge ko demonstrate karta hai.

## Syntax
Dependencies ke sath ek custom factory provider:
```typescript
{
  provide: MyService,
  useFactory: () => {
    const http = inject(HttpClient);
    return new MyService(http);
  }
}
```

## Code Examples
Neeche ek custom injection token aur dynamic factory provider ka implementation diya gaya hai koi configuration variables ke basis par different service instances ko resolve karta hai.

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
1. **Default to OnPush**: Change detection checks ko limit karne ke liye saare components par `ChangeDetectionStrategy.OnPush` configure karein.
2. **Use `CanMatch` to Secure Chunks**: Unauthorized users ko restricted code bundles download karne se rokne ke liye `CanMatch` functional guards ka use karke routes ko secure karein.
3. **Wrap browser-specific code in checks**: SSR compatibility ensure karne ke liye browser-specific globals (jaise `window` ya `document`) ke saare references ko platform checks me wrap karein.

## Common Mistakes
* **Mutating references inside OnPush components**: OnPush strategy use karne wale components me directly object properties ko mutate karna, jo Angular ko changes detect karne se rokta hai.
* **Creating memory leaks in HTTP interceptors**: Mock HTTP testing configurations ko clean up karna bhool jana ya silent token refreshes ke dauran infinite redirect loops create kar dena.

## Interview Questions & Answers

### Q1: How does `ChangeDetectionStrategy.OnPush` work and when should it be used?
**A**: `OnPush` strategy me Angular component aur uske children ko change detection scan se skip kar deta hai. Yeh sirf tabhi check karta hai jab: (1) Component ko parent se naya `@Input()` reference mile, (2) Component template me koi event trigger ho, ya (3) Hum manually `ChangeDetectorRef` ke zariye request karein. Performance optimize karne ke liye senior developers ise by default use karte hain.

### Q2: What is Zoneless Angular and how is it implemented?
**A**: Zoneless Angular me Zone.js library ko completely bypass kiya jata hai. Isme reactivity ke liye completely Angular Signals API ka use hota hai. Ise implement karne ke liye `zone.js` imports ko remove karte hain aur app bootstrap ke providers array me `provideExperimentalZonelessChangeDetection()` function register karte hain. Isse bundle size bohot drop ho jata hai.

### Q3: Explain how the hierarchical Dependency Injection tree works.
**A**: Angular me DI tree elements, modules, aur routes ke nested hierarchy system par resolve hota hai. Jab koi component kisi service ka demand token fetch karta hai, toh Angular sabse pehle local Component Injector me check karta hai. Agar wahan na mile, toh upward direction me navigation guards, modules, App root, aur ant me framework platform injectors par traverse karta hai jab tak token resolve na ho jaye.

### Q4: Explain the differences between the RxJS flattening operators: `switchMap`, `mergeMap`, `concatMap`, and `exhaustMap`.
**A**: 
- `switchMap`: New request aane par active network request cancel kar deta hai (live search options ke liye best).
- `mergeMap`: Parallel requests run karta hai bina kisi request cancel kiye (chat inputs).
- `concatMap`: Queue system me serial updates data stream check karta hai (transactions).
- `exhaustMap`: Current request running status me duplicate clicks (double-clicks submit actions) ignore karta hai.

### Q5: How do you handle authentication silent refreshes inside an HTTP Interceptor?
**A**: HTTP Interceptor outgoing requests me data validation verify karta hai. Jab API 401 error throw karti hai (token expire), interceptor request ko intercept karke `refreshToken` service call karta hai. Agar refresh logic se new access token generate ho jata hai, toh request update headers ke sath retry ho jati hai, warna user redirect login route par force close ho jata hai.

### Q6: What are hydration errors in SSR and how can you resolve them?
**A**: Hydration errors tab aate hain jab server-rendered HTML aur client-compiled JS DOM structure me content discrepancy (difference) ho. Ise solve karne ke liye manual DOM mutations bypass check bypass methods use karein, platform checks implement karein aur root bootstrap me `provideClientHydration()` load karein.

## Summary
Advanced level interviews runtime optimizations, custom dependency injection configurations, aur server-side rendering support par focus karte hain. In topics ko review karne se senior candidates ko unki system design capabilities demonstrate karne me help milti hai.

---

Previous : [Intermediate Interview Prep](./29_Interview_Prep_Intermediate.md) | Index : [Home](./00_index.md) | Next : [Scenario and System Design](./31_Interview_Prep_Scenario_and_System_Design.md)
