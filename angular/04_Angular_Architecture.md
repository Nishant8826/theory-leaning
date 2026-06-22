# Angular Architecture

## What is it?
Angular Architecture is a component-driven framework blueprint. It defines how views (Templates), styling (CSS), behavior (Component TypeScript), dependency injectors, and data providers (Services) compile and coordinate together to run a Single Page Application.

## Why do we need it?
Without a defined architectural model, codebases quickly descend into chaos as they grow. Developers put business logic directly in HTML templates, write duplicate HTTP requests, or build unstable component communications. Angular's architecture establishes a strict separation of concerns, ensuring each class has a clear role (Presentation, Structure, Behavior, State, or Integration).

```
┌────────────────────────────────────────────────────────┐
│                      Angular App                       │
└──────────────────────────┬─────────────────────────────┘
                           ▼
          ┌──────────────────────────────────┐
          │  bootstrapApplication(AppComponent)│
          └────────────────┬─────────────────┘
                           ▼
             ┌────────────────────────────┐
             │       Root Component       │
             │       (AppComponent)       │
             └─────────────┬──────────────┘
                           ▼
             ┌────────────────────────────┐
             │    Sub-Components Tree     │
             │  (Home, Products, Login)   │
             └─────────────┬──────────────┘
                           ▼
             ┌────────────────────────────┐
             │  Shared Services / APIs    │
             │  (Dependency Injection)    │
             └────────────────────────────┘
```

## How does it work?
1. **Bootstrapping**: When the app starts, the index file loads `main.ts`. In modern Angular, `bootstrapApplication(AppComponent, config)` runs, spinning up the primary view.
2. **Standalone Components**: The building blocks of modern Angular. They explicitly import their own dependencies, bypassing the legacy module-based container architecture (`NgModule`).
3. **Dependency Injection**: Injectors supply components with services. If a component requests a service, the DI system retrieves or instantiates it, ensuring separation of UI logic and data processing.

## Impact
* **Application Architecture**: Predictable structure. Every application is built as a nested tree of components bound to data services.
* **Performance**: Standalone components allow deep tree-shaking, resulting in smaller bundles.
* **Scalability**: Hierarchical injection tree enables lazy-loaded modules to have self-contained state.

## Real World Example
In a global banking dashboard, the UI elements (charts, tables, menus) are individual components. Authentication checks, API communication, and financial operations reside in separate shared services injected via DI only where needed.

## Syntax
Modern Angular applications configure the application bootstrap via `app.config.ts`:
```typescript
import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { provideHttpClient } from '@angular/common/http';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideHttpClient()
  ]
};
```

## Hinglish Explanation

Angular Architecture ko samajhne ke liye, ise ek bade building complex ki tarah socho:

### 1. Root Component (`app-root`)
Yeh complex ka "Main Entrance Gate" hai. Poori application me sabse pehle yahi screen par render hota hai. Iske andar baaki ke saare components (jaise login page, dashboard, sidebar) fit hote hain.

### 2. Standalone Components (Azaad Kamre)
Jaise building complex me har flat azaad hota hai aur uske paas apna gate aur utilities hoti hain, waise hi Standalone Components azaad hote hain. Inhe kisi module par depend nahi rehna padta. Agar unhe kisi helper tool (jaise pipes ya buttons) ki zaroorat hai, toh wo directly unhe import kar lete hain.

### 3. Bootstrap Application (Udhghatan)
Jab application run hoti hai, toh sabse pehle initialization process chalta hai jise bootstrap kehte hain. Yeh kaam `main.ts` file me hota hai jahan `bootstrapApplication(AppComponent, appConfig)` run hota hai. Yeh framework ko batata hai ki `AppComponent` se shuru karo aur configuration `appConfig` se loading guidelines lo.

### 4. Application Configuration (`app.config.ts`)
Yeh building ka management/reception room hai. Kaunsi lift kahan jayegi (Routing), paani/light ki pipe lines kaise chalengi (HttpClient/HTTP clients), aur doosri rules and regulations yahan configured hote hain.

## Code Examples
Below is the full implementation of a modern Standalone-centric application bootstrap architecture.

### `main.ts`
```typescript
import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));
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
      <p>Bootstrap status: Completed Successfully</p>
    </main>
  `,
  styles: [`
    .app-header { background: #1f2937; color: white; padding: 15px; text-align: center; }
    main { padding: 20px; text-align: center; font-family: sans-serif; }
  `]
})
export class AppComponent {}
```

## Best Practices
1. **Avoid Legacy Modules**: Do not write new components that rely on `NgModule`. Always set `standalone: true`.
2. **Single Instance Configs**: Provide global engines (Router, HttpClient, Store) in `appConfig` within `app.config.ts` during bootstrapping.
3. **Decouple View from Services**: Never write complex computation or business logic directly inside components. Put it in injectables.

## Common Mistakes
* **Bootstrapping multiple components**: Attempting to bootstrap multiple sibling components in `index.html`. Bootstrap a single root element (`app-root`) and structure the rest as nested child components.
* **Cyclic Dependencies**: Importing Component A inside Component B and vice-versa. Maintain a strict top-down structure or resolve cyclic issues using shared services.

## Interview Questions & Answers
### Q: What is bootstrapping in Angular, and how has it changed in modern versions?
**A**: Bootstrapping is the initialization process of loading the Angular runtime and rendering the root component. In older versions, this required an `NgModule` (`platformBrowserDynamic().bootstrapModule(AppModule)`). In modern Angular (v14+), bootstrapping is direct and uses the standalone API `bootstrapApplication(AppComponent, appConfig)`.
* **Hinglish Explanation**: Bootstrapping Angular application ko start karne (load karne) ka initialization process hai, jisse Angular runtime activate hota hai aur screen par root component render hota hai. Pehle bootstrapping karne ke liye `NgModule` ki zaroorat hoti thi (`bootstrapModule(AppModule)` chalana padta tha). Lekin modern Angular (v14+) me standalone API `bootstrapApplication(AppComponent, appConfig)` ka use karke direct bootstrapping hoti hai, jisse application lightweight ho jati hai.

### Q: What are Standalone Components, and what problem do they solve?
**A**: Standalone components are components that do not require an intermediate `NgModule` wrapper. They declare `standalone: true` and specify their dependencies directly in their `imports` array.
* **Hinglish Explanation**: Standalone components bina kisi extra module (`NgModule`) ke kaam kar sakte hain. Yeh component metadata me `standalone: true` declare karte hain aur apni zaroorat ki dependencies (jaise doosre components ya directives) ko directly `imports: [...]` block me specify kar dete hain. Isse modules banane ka jhanjhat khatam hota hai aur custom components ko share karna simple ho jata hai.

## Summary
The modern Angular architecture leverages Standalone components and a centralized application config. Bootstrapped directly via TypeScript, this approach separates visual display from services and API calls using Dependency Injection.

---

Previous : [TypeScript Fundamentals](./03_Typescript_Fundamentals.md) | Index : [Home](./00_index.md) | Next : [Components and Templates](./05_Components_and_Templates.md)
