# Scenario and System Design

## What is it?
Scenario and System Design un architectural scenarios, performance issues, aur structural design choices ka compilation hai jise developers large-scale Angular applications design karte waqt face karte hain.

## Why do we need it?
In senior engineering interviews, candidates ko aksar unki systems design karne ki ability par evaluate kiya jata hai, na ki sirf code likhne par. System design scenarios—jaise real-time dashboards design karna, massive list updates manage karna, multi-tenant routing configure karna, aur large monorepos set up karna—ko review karne se senior developers ko apne planning aur architectural skills demonstrate karne me help milti hai.

```
System Design Flow:
Define Requirements ──> Choose Reactivity Model (Signals/RxJS) ──> Establish Domain Boundaries
                     ──> Plan State Caching ──> Configure Lazy Loading ──> Optimize Rendering
```

## How does it work?
1. **System Modeling**: Requirements, domains, aur data flows ko identify karta hai.
2. **Reactivity Selection**: Signals (state tracking ke liye) aur RxJS (event streams ke liye) ke beech choose karta hai.
3. **Optimizations Planning**: Rendering strategies (jaise OnPush aur virtual scrolling) aur lazy-loading configurations recommend karta hai.

## Impact
* **Application Architecture**: Tight coupling ko rokta hai, jisse domain features clean aur maintain karne me easy rehte hain.
* **Performance**: Aisi optimizations ko promote karta hai jo page load times ko fast rakhti hain aur heavy use ke dauran interfaces ko responsive banaye rakhti hain.
* **Scalability**: Large monorepos me multiple teams ko features independently develop karne me help karta hai.

## Real World Example
Ek architect se delivery application ke liye ek real-time tracking dashboard design karne ko kaha jata hai. Architect ka design incoming events ke liye WebSockets ko RxJS streams se map karta hai, active state ko manage karne ke liye Writable Signals ka use karta hai, aur rendering updates ko efficiently trigger karne ke liye computed signals ka use karta hai.

## Syntax
Domains map karne ke liye ek enterprise monorepos (Nx) structure:
```
apps/
  ├── store-front/         # Customer application
  └── admin-panel/         # Administrative panel
libs/
  ├── shared/ui/           # Reusable UI elements
  └── billing/domain/      # Isolated billing logic library
```

## Code Examples
Neeche ek real-time event coordinator ka implementation diya gaya hai jo stream events ko log aur throttle karta hai, aur system coordination logic ko demonstrate karta hai.

```typescript
import { Injectable } from '@angular/core';
import { Subject, Observable } from 'rxjs';
import { throttleTime, map } from 'rxjs/operators';

export interface TelemetryEvent {
  metric: string;
  value: number;
}

@Injectable({
  providedIn: 'root'
})
export class TelemetryCoordinator {
  private telemetry$ = new Subject<TelemetryEvent>();

  // Expose throttled events to components
  events$: Observable<TelemetryEvent> = this.telemetry$.pipe(
    throttleTime(500), // Throttle to prevent rendering overload
    map(evt => ({ ...evt, value: Math.round(evt.value) }))
  );

  dispatch(event: TelemetryEvent) {
    this.telemetry$.next(event);
  }
}
```

## Best Practices
1. **Isolate Domain Logic**: Core domains (jaise checkout aur catalog) ko isolated folders ya libraries me rakhein taaki unnecessary dependencies se bacha ja sake.
2. **Throttle Heavy Event Streams**: Throttling operators (jaise `throttleTime` ya `sampleTime`) ka use karein taaki real-time streams UI ko overload na karein.
3. **Default to Lazy Loading**: Initial bundles ko chota aur page loads ko fast rakhne ke liye saare feature components ko lazy load karein.

## Common Mistakes
* **Monolithic State Models**: Pure application state ko ek hi global store me save karna, jisse codebase ko maintain karna mushkil ho jata hai.
* **Direct DOM Mutations**: DOM ko directly modify karne ke liye Angular ke renderer ko bypass karna, jo rendering bugs aur security issues create kar sakta hai.

## Interview Questions & Answers

### Q1: Design a real-time financial trading dashboard. How would you handle incoming WebSocket price updates?
**A**: Iske liye hum ek layered architecture design karenge:
1. **Data Layer**: Ek singleton service WebSocket connection banayegi aur raw real-time stream ko RxJS Observable me expose karegi.
2. **State Layer**: Is stream ko `throttleTime(300)` aur `distinctUntilChanged` jaise operators ke zariye control kiya jayega taaki screen refresh overload na ho. Throttled data se hum central Signal Store ya Writable Signals update karenge.
3. **UI Layer**: Components me `OnPush` strategy use karenge aur read-only computed signals use karenge taaki updates fast ho aur unnecessary change detection cycles na chalein.

### Q2: Design a multi-tenant client portal with lazy loading and tenant-specific configurations.
**A**: 
1. **Core Configuration**: Dynamic configuration variables (jaise theme aur API endpoints) ko app startup ke time `InjectionToken` ke zariye bootstrap providers me inject karenge.
2. **Routing Structure**: Har tenant ke specific modules (e.g. billing, dashboard) ko route config me `loadComponent` ke zariye dynamically lazy load karenge.
3. **Authentication**: Functional route guards (`CanMatch`) ka use karke permissions verify karenge taaki user bina authorization ke code bundles download na kar sake.

### Q3: How do you design state caching for API requests?
**A**: State caching ke liye hum ek HTTP Interceptor ya Dedicated Cache Service design karenge. Jab bhi koi GET request jayegi, interceptor use catch karega aur cache Map check karega. Agar cached response valid hai, toh wahi se data return ho jayega. Agar cache expire ho chuka hai, tabhi actual HTTP call chalegi aur dynamic response se local cache coordinate updates update ho jayenge.

### Q4: Design a large monorepos structure for an enterprise organization.
**A**: Enterprise scalability ke liye hum Nx monorepo framework use karenge:
- **`apps/`**: Isme micro-frontend portals ke shells (jaise customer-shell, admin-shell) hote hain jo routing manage karte hain.
- **`libs/`**: Isme shared library modules honge, jaise:
  - `libs/shared/ui/` (common inputs, buttons).
  - `libs/shared/data-access/` (common API handlers).
  - `libs/domains/` (billing, catalog business logic libraries).
- Aur lint border boundaries tags set karenge taaki alag-alag domain modules direct aapas me dynamic imports lock na karein.

### Q5: How would you debug an application that has a slow First Contentful Paint (FCP) time?
**A**: Slow FCP (First Contentful Paint) debug karne ke steps:
1. **Bundle Analysis**: `source-map-explorer` se check karenge ki kaunsi heavy packages bundle size badha rahi hain.
2. **Lazy Loading**: Ensure karenge ki saare page routes dynamic `loadComponent` use kar rahe hain.
3. **Server rendering (SSR)**: Provide client hydration aur SSR active configure karenge taaki initial page loading static screen direct server side se appear ho.
4. **Media Optimization**: Images compress karenge aur priority critical images ko preload code links me apply karenge.

### Q6: How do you prevent layout shifts during hydration?
**A**: Hydration layout shifts se bachne ke liye:
1. Browser specific calculations window/document variables access dynamic platform check `isPlatformBrowser` me set karein.
2. Client browser compilation me direct native DOM change codes (manipulations) avoid karein.
3. App bootstrap step par `provideClientHydration()` configure karein.
4. Heavy items (ads ya graphs templates) ke layout area dimensions CSS heights me secure reserve parameters rakhein.

## Summary
Scenario aur System Design evaluations planning aur architectural skills ko test karte hain. Real-time data handling, state caching, aur monorepos layouts jaise topics ko review karne se candidates senior engineering discussions ke liye prepare hote hain.

---

Previous : [Advanced Interview Prep](./30_Interview_Prep_Advanced.md) | Index : [Home](./00_index.md) | Next : [Index](./00_index.md)
