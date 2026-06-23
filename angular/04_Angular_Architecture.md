# Angular Architecture

## What is it?
Angular Architecture component-driven framework ka ek blueprint hai. Yeh define karta hai ki kaise views (Templates), styling (CSS), behavior (Component TypeScript), dependency injectors, aur data providers (Services) aapas me compile aur coordinate hokar Single Page Application run karte hain.

## Why do we need it?
Bina kisi clear architectural model ke, jaise-jaise codebase bada hota hai, chaos badh jata hai. Developers business logic HTML templates me likh de sakte hain, duplicate HTTP requests banate hain, ya fir unstable component communication setup karte hain. Angular ka architecture strict separation of concerns (kaam ka bantwara) establish karta hai, jisse yeh ensure hota hai ki har class ka ek clear role (Presentation, Structure, Behavior, State, ya Integration) ho.

```
┌────────────────────────────────────────────────────────┐
│                      Angular App                       │
│└──────────────────────────┬─────────────────────────────┘
│                           ▼
│          ┌──────────────────────────────────┐
│          │  bootstrapApplication(AppComponent)│
│          └────────────────\u252c─────────────────┘
│                            ▼
│              ┌────────────────────────────┐
│              │       Root Component       │
│              │       (AppComponent)       │
│              └─────────────┬──────────────┘
│                            ▼
│              ┌────────────────────────────┐
│              │    Sub-Components Tree     │
│              │  (Home, Products, Login)   │
│              └─────────────┬──────────────┘
│                            ▼
│              ┌────────────────────────────┐
│              │  Shared Services / APIs    │
│              │  (Dependency Injection)    │
│              └────────────────────────────┘
```

## How does it work?
1. **Bootstrapping**: Jab app start hoti hai, toh index file load hone ke baad `main.ts` execute hota hai. Modern Angular me, `bootstrapApplication(AppComponent, config)` run hota hai aur primary root view generate karta hai.
2. **Standalone Components**: Modern Angular ke building blocks. Yeh modular container structure (`NgModule`) ko bypass karke apni dependency imports metadata me khud declare karte hain.
3. **Dependency Injection**: Injector system components ko services supply karta hai. Jab koi component kisi service ki request karta hai, toh DI system use retrieve ya instantiate karke provide karta hai, jo UI templates aur data processing logic ka clear separation banaye rakhta hai.

## Impact
* **Application Architecture**: Predictable structure milta hai. Har application components ka ek nested tree hoti hai jo shared data services se connected hoti hai.
* **Performance**: Standalone components code splitting aur deep tree-shaking support karte hain, jisse compiled bundle size kaafi small ho jata hai.
* **Scalability**: Hierarchical injection tree lazy-loaded modules ko self-contained state maintain karne ki permission deti hai.

## Real World Example
Ek global banking dashboard project me, visual dashboard elements (charts, tables, menus) individual components होते हैं. Jabki authentication status, API calls, aur financial calculations alag services directories me hote hain jinhe DI ke through import kiya jata hai.

## Syntax
Modern Angular applications configuration bootstrap settings `app.config.ts` me setup karte hain:
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

## Code Examples
Neeche Standalone-centric bootstrap app framework ka complete implementation diya gaya hai:

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
1. **Avoid Legacy Modules**: Naye components likhte waqt `NgModule` use na karein. Humesha `standalone: true` set karein.
2. **Single Instance Configs**: Global engines (Router, HttpClient, Store) ko application bootstrapping ke waqt `app.config.ts` ke `appConfig` me register karein.
3. **Decouple View from Services**: Components ke andar kabhi bhi complex computations ya business calculations directly na likhein. Ise humesha separate services me delegate karein.

## Common Mistakes
* **Bootstrapping multiple components**: `index.html` me directly multiple sibling components ko bootstrap karne ki koshish karna. Humesha ek single root component (`app-root`) bootstrap karein aur baaki component templates ko nesting child trees ke roop me layout karein.
* **Cyclic Dependencies**: Component A me Component B ko import karna aur B me A ko. Humesha top-down structure setup rakhein ya cyclic issue handle karne ke liye shared service inject karein.

## Interview Questions & Answers
### Q: What is bootstrapping in Angular, and how has it changed in modern versions?
**A**: Bootstrapping Angular runtime ko initialize aur root component ko render karne ka process hai. Purane versions me, iske liye `NgModule` setup chahiye hota tha (`platformBrowserDynamic().bootstrapModule(AppModule)`). Modern Angular (v14+) me, bootstrapping direct aur lightweight standalone API `bootstrapApplication(AppComponent, appConfig)` ke zariye hoti hai.

### Q: What are Standalone Components, and what problem do they solve?
**A**: Standalone components aise components hote hain jinhe kisi intermediate `NgModule` wrapper ki zaroorat nahi padti. Yeh metadata me `standalone: true` set karte hain aur direct dependencies ko `imports` array me specify kar lete hain.

## Summary
Modern Angular architecture Standalone components aur centralized application config structure par based hai. TypeScript se boot hone wala yeh setup DI ke zariye rendering view aur API/business logic ko separate rakhta hai.

---

Previous : [TypeScript Fundamentals](./03_Typescript_Fundamentals.md) | Index : [Home](./00_index.md) | Next : [Components and Templates](./05_Components_and_Templates.md)
