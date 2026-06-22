# Scenario and System Design

## What is it?
Scenario and System Design compiles architectural scenarios, performance issues, and structural design choices that developers encounter when designing large-scale Angular applications.

## Why do we need it?
In senior engineering interviews, candidates are often evaluated on their ability to design systems, rather than just write code. Reviewing system design scenarios—such as designing real-time dashboards, managing massive list updates, configuring multi-tenant routing, and setting up large monorepos—helps senior developers demonstrate their planning and architectural skills.

```
System Design Flow:
Define Requirements ──> Choose Reactivity Model (Signals/RxJS) ──> Establish Domain Boundaries
                     ──> Plan State Caching ──> Configure Lazy Loading ──> Optimize Rendering
```

## How does it work?
1. **System Modeling**: Identifies requirements, domains, and data flows.
2. **Reactivity Selection**: Chooses between Signals (for state tracking) and RxJS (for event streams).
3. **Optimizations Planning**: Recommends rendering strategies (like OnPush and virtual scrolling) and lazy-loading configurations.

## Impact
* **Application Architecture**: Prevents tight coupling, keeping domain features clean and easy to maintain.
* **Performance**: Promotes optimizations that keep load times fast and interfaces responsive under heavy use.
* **Scalability**: Enables multiple teams to develop features independently in large monorepos.

## Real World Example
An architect is asked to design a real-time tracking dashboard for a delivery application. The architect design uses WebSockets mapped to RxJS streams for incoming events, Writable Signals to manage active state, and computed signals to trigger rendering updates efficiently.

## Syntax
An enterprise monorepos (Nx) structure mapping domains:
```
apps/
  ├── store-front/         # Customer application
  └── admin-panel/         # Administrative panel
libs/
  ├── shared/ui/           # Reusable UI elements
  └── billing/domain/      # Isolated billing logic library
```

## Hinglish Explanation

Scenario aur System Design interviews me code-level solutions ke bajaye application architecture decisions aur scaling algorithms pooche jate hain:

### 1. Real-time dashboard architecture (WebSockets)
* WebSockets direct connect karke dynamic updates check karna UI page ko hang kar sakta hai. Isliye state layer design karte waqt hum raw streams ko standard filter functions (`throttleTime(500)`) se pass karte hain aur state sync ke liye read-only signals read karte hain jisse page slow na ho.

### 2. HTTP API caching system
* Backend API resources minimize karne ke liye caching interceptors use hote hain jo dynamic GET queries local Map storage caching patterns me trace karte hain. Valid timestamp status tak data direct client memory se load hota hai bina background execution delay ke.

### 3. Enterprise Monorepo pattern (Nx)
* Multi-applications and multi-teams projects single repository me workspace build karte hain. Hum boundaries rules set karke modules code leakage cross domains restrict karte hain taaki billing library profile data objects direct touch na kare.

## Code Examples
Below is an implementation of a real-time event coordinator that logs and throttle stream events, demonstrating system coordination logic.

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
1. **Isolate Domain Logic**: Keep core domains (like checkout and catalog) isolated in separate folders or libraries to prevent dependencies.
2. **Throttle Heavy Event Streams**: Use throttling operators (like `throttleTime` or `sampleTime`) to prevent real-time streams from overloading the UI.
3. **Default to Lazy Loading**: Lazy load all feature components to keep initial bundles small and page loads fast.

## Common Mistakes
* **Monolithic State Models**: Storing all application state in a single global store, making the codebase hard to maintain.
* **Direct DOM Mutations**: Bypassing Angular's renderer to modify the DOM directly, which can cause rendering bugs and security issues.

## Interview Questions & Answers

### Q1: Design a real-time financial trading dashboard. How would you handle incoming WebSocket price updates?
**A**: I would use a layered architecture:
1. **Data Layer**: An injectable service manages the WebSocket connection, exposing the raw event stream as an RxJS Observable.
2. **State Layer**: The stream is piped through operators (like `throttleTime` and `distinctUntilChanged`) to prevent rendering overload. The throttled events update a central `NgRx Signal Store` or Writable Signals.
3. **UI Layer**: Presentation components use `ChangeDetectionStrategy.OnPush` and read from read-only computed signals, keeping change detection checks minimal and updates fast.
* **Hinglish Explanation**: Iske liye hum ek layered architecture design karenge:
  1. **Data Layer**: Ek singleton service WebSocket connection banayegi aur raw real-time stream ko RxJS Observable me expose karegi.
  2. **State Layer**: Is stream ko `throttleTime(300)` aur `distinctUntilChanged` jaise operators ke zariye control kiya jayega taaki screen refresh overload na ho. Throttled data se hum central Signal Store ya Writable Signals update karenge.
  3. **UI Layer**: Components me `OnPush` strategy use karenge aur read-only computed signals use karenge taaki updates fast ho aur unnecessary change detection cycles na chalein.

### Q2: Design a multi-tenant client portal with lazy loading and tenant-specific configurations.
**A**: I would design the portal as follows:
1. **Core Configuration**: Use an `InjectionToken` to inject tenant-specific configurations (like theme variables and API endpoints) during bootstrapping.
2. **Routing Structure**: Lazy load domains (like billing and settings) using `loadComponent`.
3. **Authentication**: Use functional route guards (`CanMatch`) to check user permissions and redirect unauthorized access before code bundles download.
* **Hinglish Explanation**: 
  1. **Core Configuration**: dynamic configuration variables (jaise theme aur API endpoints) ko app startup ke time `InjectionToken` ke zariye bootstrap providers me inject karenge.
  2. **Routing Structure**: Har tenant ke specific modules (e.g. billing, dashboard) ko route config me `loadComponent` ke zariye dynamically lazy load karenge.
  3. **Authentication**: Functional route guards (`CanMatch`) ka use karke permissions verify karenge taaki user bina authorization ke code bundles download na kar sake.

### Q3: How do you design state caching for API requests?
**A**: I would implement state caching using an HTTP Interceptor or a dedicated caching service. The interceptor intercepts outgoing GET requests, checks a cache Map for stored responses, and returns them immediately if they are still valid. If the cache is expired, it makes the API call and updates the cache, keeping network requests minimal.
* **Hinglish Explanation**: State caching ke liye hum ek HTTP Interceptor ya Dedicated Cache Service design karenge. Jab bhi koi GET request jayegi, interceptor use catch karega aur cache Map check karega. Agar cached response valid hai, toh wahi se data return ho jayega. Agar cache expire ho chuka hai, tabhi actual HTTP call chalegi aur dynamic response se local cache coordinate updates update ho jayenge.

### Q4: Design a large monorepos structure for an enterprise organization.
**A**: I would use a monorepos framework like Nx:
- **`apps/`**: Contains thin application shells (like customer portal and admin panel) that orchestrate routing and bootstrap domains.
- **`libs/`**: Contains shared libraries:
  - `libs/shared/ui/`: Reusable UI elements (buttons, inputs).
  - `libs/shared/data-access/`: Core API clients and security handlers.
  - `libs/domains/`: Domain libraries (billing, catalog) that manage their own state and components.
- Configure dependency rules to prevent domains from importing private files from other domains.
* **Hinglish Explanation**: Enterprise scalability ke liye hum Nx monorepo frame use karenge:
  - **`apps/`**: Isme micro-frontend portals ke shells (jaise customer-shell, admin-shell) hote hain jo routing manage karte hain.
  - **`libs/`**: Isme shared library modules honge, jaise:
    - `libs/shared/ui/` (common inputs, buttons).
    - `libs/shared/data-access/` (common API handlers).
    - `libs/domains/` (billing, catalog business logic libraries).
  - Aur lint border boundaries tags set karenge taaki alag-alag domain modules direct aapas me dynamic imports lock na karein.

### Q5: How would you debug an application that has a slow First Contentful Paint (FCP) time?
**A**: I would take the following steps:
1. **Analyze Bundle Sizes**: Run `source-map-explorer` to identify heavy dependencies.
2. **Configure Lazy Loading**: Verify that all route components are lazy-loaded on-demand using `loadComponent`.
3. **Implement SSR**: Set up Server-Side Rendering (SSR) and hydration to deliver pre-rendered HTML templates immediately, accelerating first-paint times.
4. **Optimize Assets**: Compress images and pre-load critical assets.
* **Hinglish Explanation**: Slow FCP (First Contentful Paint) debug karne ke steps:
  1. **Bundle Analysis**: `source-map-explorer` se check karenge ki kaunsi heavy packages bundle size badha rahi hain.
  2. **Lazy Loading**: Ensure karenge ki saare page routes dynamic `loadComponent` use kar rahe hain.
  3. **Server rendering (SSR)**: provide client hydration and SSR active configure karenge taaki initial page loading static screen direct server side se appear ho.
  4. **Media Optimization**: Images compress karenge aur priority critical images ko preload code links me apply karenge.

### Q6: How do you prevent layout shifts during hydration?
**A**: I would prevent layout shifts by:
1. Wrap browser-specific calls in `isPlatformBrowser` checks.
2. Avoiding manual DOM mutations on the client.
3. Using `provideClientHydration()` during bootstrapping.
4. Reserving layout spaces for dynamic components (like ads or charts) using CSS styles.
* **Hinglish Explanation**: Hydration layout shifts se bachne ke liye:
  1. Browser specific calculations window/document variables access dynamic platform check `isPlatformBrowser` me set karein.
  2. Client browser compilation me direct native DOM change codes (manipulations) avoid karein.
  3. App bootstrap step par `provideClientHydration()` configure karein.
  4. Heavy items (ads ya graphs templates) ke layout area dimensions CSS heights me secure reserve parameters rakhein.

## Summary
Scenario and System Design evaluations test your planning and architectural skills. Reviewing topics like real-time data handling, state caching, and monorepos layouts helps candidates prepare for senior engineering discussions.

---

Previous : [Advanced Interview Prep](./30_Interview_Prep_Advanced.md) | Index : [Home](./00_index.md) | Next : [Index](./00_index.md)
