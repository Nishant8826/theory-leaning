# 🅰️ Angular – Complete Revision Guide & Master Cheat Sheet

Welcome to the comprehensive Angular Master Revision Sheet. This single document compiles all core architectural concepts, modern Standalone patterns, Signals, RxJS operators, lifecycle phases, enterprise best practices, and interview takeaways across all 26 topics.

Each section is designed to be **self-sufficient and easy to understand**, so you have all the essential explanations, analogies, rules, and code patterns in one place without needing to navigate individual lesson files.

---

## 📌 Module Navigation
- [01. Introduction to Angular](#01-introduction-to-angular)
- [02. Setup and Environment](#02-setup-and-environment)
- [03. TypeScript Fundamentals](#03-typescript-fundamentals)
- [04. Angular Architecture](#04-angular-architecture)
- [05. Components and Templates](#05-components-and-templates)
- [06. Pipes](#06-pipes)
- [07. Directives](#07-directives)
- [08. Component Lifecycle](#08-component-lifecycle)
- [09. Component Communication](#09-component-communication)
- [10. Signals](#10-signals)
- [11. Dependency Injection](#11-dependency-injection)
- [12. Services and Business Logic](#12-services-and-business-logic)
- [13. Routing and Navigation](#13-routing-and-navigation)
- [14. Template-Driven Forms](#14-template-driven-forms)
- [15. Reactive Forms](#15-reactive-forms)
- [16. HttpClient and API Integration](#16-httpclient-and-api-integration)
- [17. RxJS Reactive Programming](#17-rxjs-reactive-programming)
- [18. State Management](#18-state-management)
- [19. Authentication and Authorization](#19-authentication-and-authorization)
- [20. Angular Material](#20-angular-material)
- [21. Performance Optimization](#21-performance-optimization)
- [22. Testing (Jasmine & Jest)](#22-testing-jasmine--jest)
- [23. Security Best Practices](#23-security-best-practices)
- [24. SSR and Advanced Concepts](#24-ssr-and-advanced-concepts)
- [25. Enterprise Architecture](#25-enterprise-architecture)
- [26. Deployment and CI/CD](#26-deployment-and-ci-cd)

---

## 01. Introduction to Angular
🔗 **Full Lesson:** [01_Introduction_to_Angular.md](./01_Introduction_to_Angular.md)

* **Core Concept**: Angular is an enterprise-grade, opinionated frontend framework developed by Google. Built on TypeScript, it provides a complete, standardized ecosystem including routing, state handling, forms, testing, and HTTP communication out of the box.
* **Real-World Analogy**: A **Custom Smart Home**. It comes pre-wired with structural plumbing (Dependency Injection), electrical circuits (Router), and thermostat controls (HttpClient). You only need to add interior decorations (Components).
* **Key Takeaways & Interview Gotchas**:
  * **Angular vs. React**: React is a UI rendering library that relies on external community packages for routing, forms, and state. Angular is a full-featured framework enforcing structural consistency across large teams.
  * **Rendering & Change Detection**: React reconciles changes using a Virtual DOM diffing tree. Angular directly compiles templates to JavaScript via the **Ivy compiler** and updates specific DOM nodes via Change Detection (Zone.js or Zoneless Signals).
  * **Modern Angular**: Uses standalone components, functional guards/interceptors, Signals for fine-grained reactivity, and `@if`/`@for` control flow blocks.

```typescript
// Standalone Component Example
import { Component } from '@angular/core';

@Component({
  selector: 'app-home',
  standalone: true,
  template: `<h1>Hello, {{ username }}!</h1>`
})
export class HomeComponent {
  username = 'Developer';
}
```

---

## 02. Setup and Environment
🔗 **Full Lesson:** [02_Setup_and_Environment.md](./02_Setup_and_Environment.md)

* **Core Concept**: Angular CLI (`@angular/cli`) automates project initialization, code scaffolding, dev-server hosting, unit testing, and production builds with tree-shaking and minification.
* **Real-World Analogy**: An **Automated Factory Assembly Line**. Instead of manually crafting individual gears and wiring files by hand, you operate a central control console (CLI) that outputs pre-tested, standardized modules directly into your project.
* **Key Takeaways & Interview Gotchas**:
  * `angular.json`: Workspace configuration file defining build targets, asset paths, global styles/scripts, and optimization settings.
  * `tsconfig.json`: TypeScript compiler options (strict mode, path aliases, target ECMAScript versions).
  * `ng build --configuration production`: Performs Ahead-Of-Time (AOT) compilation, dead-code elimination (tree-shaking), CSS/JS minification, and output hashing for cache busting.

```bash
# Essential CLI Commands
npm install -g @angular/cli                              # Global CLI installation
ng new my-app --standalone --style=css                   # Scaffolds new standalone app
ng serve --port 4200 --open                              # Runs local dev server with Hot Reload
ng generate component components/user-profile            # Generates component files (c)
ng generate service services/auth                        # Generates service and test file (s)
ng build --configuration production                      # Compiles production bundle in dist/
```

---

## 03. TypeScript Fundamentals
🔗 **Full Lesson:** [03_Typescript_Fundamentals.md](./03_Typescript_Fundamentals.md)

* **Core Concept**: TypeScript adds static type definitions to JavaScript, catching syntax errors, data mismatches, and broken contracts at compile time before deployment.
* **Real-World Analogy**: **Construction Blueprints**. Checking blueprint specifications before pouring concrete prevents discovering structural misalignments after the building is completed.
* **Key Takeaways & Interview Gotchas**:
  * **`interface` vs `type`**:
    * Use `interface` for defining object models, public API shapes, and class contracts because they support declaration merging and OOP `implements`/`extends`.
    * Use `type` for union types (`'admin' | 'user'`), intersection types, tuples, primitives, or utility mappings (`Partial<T>`, `Pick<T, K>`, `Record<K, T>`).
  * **Access Modifiers**: `public` (default, accessible anywhere), `private` (accessible only inside declaring class), `protected` (accessible inside class and subclasses), `readonly` (immutable after initialization).

```typescript
// Interfaces, Generics, and Utility Types
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

type ApiResponse<T> = {
  data: T;
  status: number;
  error?: string;
};

// Generic API fetching function
async function fetchData<T>(url: string): Promise<ApiResponse<T>> {
  const res = await fetch(url);
  return res.json();
}
```

---

## 04. Angular Architecture
🔗 **Full Lesson:** [04_Angular_Architecture.md](./04_Angular_Architecture.md)

* **Core Concept**: Modern Angular architecture is modular and component-driven. Standalone components declare their own dependencies (`imports: [...]`), eliminating legacy `NgModule` boilerplate and drastically improving tree-shaking.
* **Real-World Analogy**: A **Self-Sufficient Smart Village**. Instead of relying on a single central power distributor (`NgModule`), every house possesses its own solar panels and battery backup (Standalone components declaring their specific dependencies).
* **Key Takeaways & Interview Gotchas**:
  * **Application Bootstrapping**: Modern applications boot using `bootstrapApplication(AppComponent, appConfig)` in `main.ts`.
  * **`appConfig` (`ApplicationConfig`)**: Central place to configure application-wide providers (e.g., `provideRouter(routes)`, `provideHttpClient(withInterceptors([...]))`).
  * **Key Building Blocks**: Components (views), Directives (DOM behavior/structure), Pipes (data formatting), Services (business logic & APIs), and Dependency Injection (wiring).

```typescript
// main.ts - Modern Standalone Bootstrapping
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));
```

---

## 05. Components and Templates
🔗 **Full Lesson:** [05_Components_and_Templates.md](./05_Components_and_Templates.md)

* **Core Concept**: Components combine presentation markup (HTML), component logic (TypeScript class), and styling (CSS) into isolated, reusable UI blocks.
* **Real-World Analogy**: A **Vehicle Instrument Panel**. The engine controller (TypeScript class) updates speedometer readings (Property Binding) and registers driver button clicks (Event Binding).
* **Key Takeaways & Interview Gotchas**:
  * **Binding Syntax Types**:
    1. `{{ value }}` : **Interpolation** (Component -> View).
    2. `[property]="value"` : **Property Binding** (Component -> DOM property).
    3. `(event)="handler()"` : **Event Binding** (View -> Component method).
    4. `[(ngModel)]="property"` : **Two-Way Binding** (Syncs input and variable simultaneously).
    5. `#refVar` : **Template Reference Variable** (Reference to DOM node or component).
  * **Modern Built-in Control Flow**: Replaces `*ngIf`, `*ngFor`, and `*ngSwitch` with `@if`, `@else if`, `@else`, `@for (item of items; track item.id)`, `@empty`, and `@switch` / `@case`.

```html
<!-- Modern Control Flow & Binding Syntax -->
<h2>Welcome, {{ user.name }}</h2>

@if (isLoggedIn) {
  <img [src]="user.avatarUrl" alt="Avatar" />
  <button (click)="logout()">Sign Out</button>
} @else {
  <p>Please log in to continue.</p>
}

<ul>
  @for (task of tasks; track task.id) {
    <li>{{ task.title }}</li>
  } @empty {
    <li>No tasks available.</li>
  }
</ul>
```

---

## 06. Pipes
🔗 **Full Lesson:** [06_Pipes.md](./06_Pipes.md)

* **Core Concept**: Pipes transform and format dynamic data directly inside HTML templates without modifying the underlying data in the TypeScript class.
* **Real-World Analogy**: **Water Filtration Nozzles**. Water flows through the same pipe; different attached nozzles transform the flow into mist, jet, or shower spray without altering the water source.
* **Key Takeaways & Interview Gotchas**:
  * **Pure Pipes (Default)**: Execute **only** when the input value's primitive or reference address changes. Highly performant because output is memoized/cached.
  * **Impure Pipes (`pure: false`)**: Execute on **every single change detection cycle**, which can cause performance bottlenecks if doing heavy calculations.
  * **`AsyncPipe` (`| async`)**: Automatically subscribes to an `Observable` or `Promise`, renders the latest value, and **automatically unsubscribes** when the component is destroyed, preventing memory leaks.

```typescript
// Custom Pure Pipe Example
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'truncate',
  standalone: true,
  pure: true // Default: pure pipe
})
export class TruncatePipe implements PipeTransform {
  transform(value: string, limit: number = 20): string {
    if (!value) return '';
    return value.length > limit ? value.substring(0, limit) + '...' : value;
  }
}
```

```html
<!-- Built-in Pipes Usage -->
<p>Price: {{ 49.99 | currency:'USD' }}</p>
<p>Date: {{ today | date:'mediumDate' }}</p>
<p>Data Stream: {{ liveData$ | async }}</p>
<p>Shortened: {{ longBio | truncate:30 }}</p>
```

---

## 07. Directives
🔗 **Full Lesson:** [07_Directives.md](./07_Directives.md)

* **Core Concept**: Directives extend HTML capabilities by attaching custom behavior or modifying DOM structure and appearance.
* **Real-World Analogy**: **Wearable Sensor Badges**. Pinning an RFID badge onto an employee triggers door unlocks or security alarms when entering specific zones without altering the employee.
* **Key Takeaways & Interview Gotchas**:
  * **Attribute Directives**: Change the appearance or behavior of an existing element (e.g., `ngClass`, `ngStyle`, custom hover highlight).
  * **Structural Directives**: Add or remove elements from the DOM (e.g., legacy `*ngIf`, `*ngFor` using `TemplateRef` and `ViewContainerRef`; replaced by `@if`/`@for` in modern Angular).
  * **Host Decorators**:
    * `@HostBinding('style.color')`: Binds a host element's CSS style or property to a directive property.
    * `@HostListener('mouseenter')`: Listens to DOM events emitted on the host element.

```typescript
// Custom Attribute Directive
import { Directive, HostBinding, HostListener } from '@angular/core';

@Directive({
  selector: '[appHighlight]',
  standalone: true
})
export class HighlightDirective {
  @HostBinding('style.backgroundColor') bgColor = 'transparent';

  @HostListener('mouseenter') onMouseEnter() {
    this.bgColor = 'yellow';
  }

  @HostListener('mouseleave') onMouseLeave() {
    this.bgColor = 'transparent';
  }
}
```

---

## 08. Component Lifecycle
🔗 **Full Lesson:** [08_Component_Lifecycle.md](./08_Component_Lifecycle.md)

* **Core Concept**: The series of stages a component goes through from instantiation to destruction. Angular provides lifecycle hooks to execute custom logic at precise moments.
* **Real-World Analogy**: **Theatrical Play Production**. Setting stage lights (`ngOnInit`), adjusting lines when cues change (`ngOnChanges`), verifying props placement (`ngAfterViewInit`), and taking down the set when the show closes (`ngOnDestroy`).
* **Key Takeaways & Interview Gotchas**:
  * **Lifecycle Order**:
    1. `constructor()`: TypeScript class instantiation & dependency injection. (Never place API calls here).
    2. `ngOnChanges()`: Runs before `ngOnInit` and whenever input bindings (`@Input()`) change reference. Receives a `SimpleChanges` object.
    3. `ngOnInit()`: Component initialization. **Best place for initial API calls and data fetching**.
    4. `ngDoCheck()`: Runs on every change detection cycle for custom change detection.
    5. `ngAfterContentInit()` / `ngAfterContentChecked()`: External content projected via `<ng-content>` is initialized/checked.
    6. `ngAfterViewInit()` / `ngAfterViewChecked()`: Component view and child views are fully rendered. Safe to access `@ViewChild` DOM queries.
    7. `ngOnDestroy()`: Cleanup phase. Essential for unsubscribing observables, stopping timers (`setInterval`), and detaching event listeners to avoid memory leaks.

```typescript
import { Component, OnInit, OnDestroy, Input, SimpleChanges, OnChanges } from '@angular/core';
import { Subscription } from 'rxjs';

@Component({ selector: 'app-lifecycle', standalone: true, template: `<p>Lifecycle</p>` })
export class LifecycleComponent implements OnInit, OnChanges, OnDestroy {
  @Input() userId!: string;
  private sub!: Subscription;

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['userId'] && !changes['userId'].firstChange) {
      this.fetchUserDetails(); // Input value changed
    }
  }

  ngOnInit(): void {
    this.fetchUserDetails(); // Initial load
  }

  ngOnDestroy(): void {
    this.sub?.unsubscribe(); // Prevent memory leak
  }

  private fetchUserDetails(): void { /* ... */ }
}
```

---

## 09. Component Communication
🔗 **Full Lesson:** [09_Component_Communication.md](./09_Component_Communication.md)

* **Core Concept**: Mechanisms to share data, state, and events across parent-child or unrelated component boundaries.
* **Real-World Analogy**: **Office Walkie-Talkies**. Managers broadcast instructions downward to team members (Inputs), while workers notify managers of completed tasks via alert beeps (Outputs).
* **Key Takeaways & Interview Gotchas**:
  * **Parent to Child**: `@Input()` property decorator or `input()` / `input.required()` Signal.
  * **Child to Parent**: `@Output()` with `EventEmitter` or `output()` function.
  * **Parent accessing Child directly**: `@ViewChild()` or `viewChild()` query.
  * **Content Projection**: Single-slot `<ng-content>` or multi-slot `<ng-content select="[header]">`.
  * **Unrelated / Cross-Tree Components**: Shared `@Injectable()` service with a `Signal` or RxJS `BehaviorSubject`.

```typescript
// Child Component
import { Component, input, output } from '@angular/core';

@Component({
  selector: 'app-user-card',
  standalone: true,
  template: `
    <h3>{{ userName() }}</h3>
    <button (click)="notifyDelete()">Delete</button>
  `
})
export class UserCardComponent {
  userName = input.required<string>();          // Signal-based required input
  userDeleted = output<string>();                // Signal-based output

  notifyDelete() {
    this.userDeleted.emit(this.userName());
  }
}
```

```html
<!-- Parent Template -->
<app-user-card [userName]="currentUserName" (userDeleted)="onUserDelete($event)"></app-user-card>
```

---

## 10. Signals
🔗 **Full Lesson:** [10_Signals.md](./10_Signals.md)

* **Core Concept**: Signals are reactive value wrappers that notify their direct consumers when updated. They provide fine-grained reactivity, allowing Angular to update only the specific DOM nodes that depend on the value without full component-tree dirty checking (enabling Zoneless Angular).
* **Real-World Analogy**: **Spreadsheet Formulas**. Changing a value in cell `A1` automatically and instantaneously recalculates dependent cell `C1` (`=A1*2`) without recalculating all unaffected cells in the entire sheet.
* **Key Takeaways & Interview Gotchas**:
  * **Writable Signal (`signal`)**: State holder modified via `.set(newValue)` or `.update(current => nextValue)`.
  * **Computed Signal (`computed`)**: Read-only, lazily evaluated, and memoized (cached) derivation of other signals. Recalculates only when its dependent signals change.
  * **Effect (`effect`)**: Runs side-effects (e.g., logging, syncing to `localStorage`) whenever any read signal inside it changes. Must run in an injection context (e.g., `constructor`).
  * **Signals vs RxJS**: Signals manage synchronous state and DOM reactivity with zero subscription management. RxJS handles complex asynchronous data streams, debouncing, and web sockets.

```typescript
import { Component, signal, computed, effect } from '@angular/core';

@Component({
  selector: 'app-counter',
  standalone: true,
  template: `
    <p>Count: {{ count() }}</p>
    <p>Double: {{ doubleCount() }}</p>
    <button (click)="increment()">Increment</button>
  `
})
export class CounterComponent {
  count = signal<number>(0);                             // Writable signal
  doubleCount = computed(() => this.count() * 2);        // Computed signal (cached)

  constructor() {
    effect(() => {
      console.log(`Count changed to: ${this.count()}`);  // Auto-tracks count()
    });
  }

  increment(): void {
    this.count.update(val => val + 1);
  }
}
```

---

## 11. Dependency Injection
🔗 **Full Lesson:** [11_Dependency_Injection.md](./11_Dependency_Injection.md)

* **Core Concept**: A design pattern where classes receive their dependencies from an external injector rather than creating them directly, promoting modularity, testability, and code reusability.
* **Real-World Analogy**: A **Central Tool Supply Room**. Instead of each builder constructing their own power drill from raw metals, they request the central tool manager (Injector) to provide a shared, pre-configured drill.
* **Key Takeaways & Interview Gotchas**:
  * **Hierarchical Injector Tree**:
    * `providedIn: 'root'`: Singleton service shared across the entire application (tree-shakeable).
    * `providers: [MyService]` in `@Component`: Creates a unique, separate service instance for that component and its child hierarchy.
  * **Modern Injection**: `inject(MyService)` can be used anywhere in an injection context (constructors, field initializers, functional guards) instead of traditional constructor parameters.

```typescript
// Service Registration
import { Injectable, inject } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class LogService {
  log(msg: string) { console.log(`[LOG]: ${msg}`); }
}

// Component Consumption using inject()
@Component({ selector: 'app-demo', standalone: true, template: `<p>DI Demo</p>` })
export class DemoComponent {
  private logger = inject(LogService); // Clean functional injection

  constructor() {
    this.logger.log('DemoComponent initialized.');
  }
}
```

---

## 12. Services and Business Logic
🔗 **Full Lesson:** [12_Services_and_Business_Logic.md](./12_Services_and_Business_Logic.md)

* **Core Concept**: Services encapsulate business logic, API requests, state manipulation, and calculation algorithms away from components, keeping UI components lightweight and focused on presentation.
* **Real-World Analogy**: **Restaurant Waiter & Kitchen**. The waiter (Component) only takes customer orders and serves plates; the kitchen (Service) manages food preparation, cooking, and ingredient sourcing.
* **Key Takeaways & Interview Gotchas**:
  * **Single Responsibility Principle (SRP)**: Components should strictly handle UI interactions and template bindings; Services should handle data transformations and external communications.
  * **State Pattern with Signals**: Keep private writable signals inside the service and expose public read-only views via `.asReadonly()` to prevent external components from mutating state directly.

```typescript
// Cart State Service Pattern
import { Injectable, signal } from '@angular/core';

export interface Product { id: number; name: string; price: number; }

@Injectable({ providedIn: 'root' })
export class CartService {
  private cartItems = signal<Product[]>([]);
  public items = this.cartItems.asReadonly(); // Read-only public access

  addToCart(product: Product): void {
    this.cartItems.update(items => [...items, product]);
  }

  removeFromCart(productId: number): void {
    this.cartItems.update(items => items.filter(p => p.id !== productId));
  }
}
```

---

## 13. Routing and Navigation
🔗 **Full Lesson:** [13_Routing_and_Navigation.md](./13_Routing_and_Navigation.md)

* **Core Concept**: Enables client-side navigation between different views in a Single Page Application (SPA) based on the browser URL without full-page reloads.
* **Real-World Analogy**: **Airport Terminals & Gates**. The main airport building remains fixed; passengers are directed to specific gates (components) based on the destination printed on their boarding pass (URL).
* **Key Takeaways & Interview Gotchas**:
  * **Lazy Loading**: `loadComponent: () => import('./path').then(m => m.Component)` splits bundle files so pages load on-demand.
  * **Functional Guards (`CanActivateFn`)**: Intercepts navigation to allow or redirect users (e.g., verifying authentication).
  * **Route Parameters**: Read path variables (`/users/:id`) via `inject(ActivatedRoute).snapshot.paramMap.get('id')`.
  * `<router-outlet>`: Placeholder directive where the routed view is rendered.

```typescript
// app.routes.ts
import { Routes, CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { AuthService } from './services/auth.service';

const authGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);
  return auth.isLoggedIn() ? true : router.createUrlTree(['/login']);
};

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { 
    path: 'dashboard', 
    loadComponent: () => import('./dashboard.component').then(m => m.DashboardComponent),
    canActivate: [authGuard] 
  },
  { 
    path: 'users/:id', 
    loadComponent: () => import('./user-detail.component').then(m => m.UserDetailComponent) 
  },
  { path: '**', loadComponent: () => import('./not-found.component').then(m => m.NotFoundComponent) }
];
```

---

## 14. Template-Driven Forms
🔗 **Full Lesson:** [14_Template_Driven_Forms.md](./14_Template_Driven_Forms.md)

* **Core Concept**: Form handling approach where form structure, models, and validation rules are declared directly inside the HTML template using `FormsModule`. Best for simple forms (login, search, contact).
* **Real-World Analogy**: **Paper Survey Forms**. You fill in predefined blank fields printed on a paper questionnaire; the structure and rules are embedded directly on the sheet.
* **Key Takeaways & Interview Gotchas**:
  * **Core Directives**: `ngModel` (binds input to property and registers control), `ngForm` (auto-attached to `<form>`), `ngModelGroup`.
  * **Validation State Classes**: Angular automatically assigns CSS classes: `ng-valid` / `ng-invalid`, `ng-touched` / `ng-untouched`, `ng-dirty` / `ng-pristine`.
  * Requires importing `FormsModule` into component `imports: [...]`.

```html
<!-- Template-Driven Form Template -->
<form #userForm="ngForm" (ngSubmit)="onSubmit(userForm)">
  <input name="email" ngModel required email #emailInput="ngModel" placeholder="Email" />
  
  @if (emailInput.invalid && emailInput.touched) {
    <span class="error">Valid email is required.</span>
  }

  <button type="submit" [disabled]="userForm.invalid">Submit</button>
</form>
```

---

## 15. Reactive Forms
🔗 **Full Lesson:** [15_Reactive_Forms.md](./15_Reactive_Forms.md)

* **Core Concept**: Programmatic, model-driven form approach where form structure, validation rules, and state are defined in TypeScript using `ReactiveFormsModule`. Best for complex, dynamic, scalable enterprise forms.
* **Real-World Analogy**: **Programmatic Spreadsheets**. Creating cell-by-cell data constraints in code, validating inputs in real-time, and computing automated formulas.
* **Key Takeaways & Interview Gotchas**:
  * **Core Classes**: `FormControl` (single field), `FormGroup` (collection of controls), `FormArray` (dynamic array of controls), `FormBuilder` (syntactic helper).
  * **`patchValue()` vs `setValue()`**:
    * `patchValue()`: Updates only specific fields; ignores missing properties safely.
    * `setValue()`: Strictly requires every field in the FormGroup to be provided or throws an error.
  * **Value / Status Streams**: Subscribe to real-time changes via `form.valueChanges` and `form.statusChanges`.

```typescript
import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="registerForm" (ngSubmit)="submit()">
      <input formControlName="email" placeholder="Email" />
      <input formControlName="password" type="password" placeholder="Password" />
      <button type="submit" [disabled]="registerForm.invalid">Register</button>
    </form>
  `
})
export class RegisterComponent {
  private fb = inject(FormBuilder);

  registerForm = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]]
  });

  submit(): void {
    if (this.registerForm.valid) {
      console.log('Submitted Payload:', this.registerForm.value);
    }
  }
}
```

---

## 16. HttpClient and API Integration
🔗 **Full Lesson:** [16_HttpClient_and_API_Integration.md](./16_HttpClient_and_API_Integration.md)

* **Core Concept**: Performs HTTP communication with backend REST APIs, automatically parsing JSON responses into strongly-typed objects and returning RxJS Observables.
* **Real-World Analogy**: A **Registered Shipping Clerk**. Inspects all outgoing packages to attach required security stamps (JWT Auth headers) and checks incoming returns for verification.
* **Key Takeaways & Interview Gotchas**:
  * **Setup**: Configured via `provideHttpClient(withInterceptors([authInterceptor]))` in `appConfig`.
  * **Functional Interceptors (`HttpInterceptorFn`)**: Central middleware to attach auth tokens, log requests, retry failed calls, or catch global errors (e.g., 401 Unauthorized).
  * **Immutable Requests**: Request objects are immutable; clone them using `req.clone({ setHeaders: { ... } })` before modifying headers.

```typescript
// Functional Auth Interceptor
import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from './auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = inject(AuthService).getToken();
  if (token) {
    req = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` }
    });
  }
  return next(req);
};
```

---

## 17. RxJS Reactive Programming
🔗 **Full Lesson:** [17_RxJS_Reactive_Programming.md](./17_RxJS_Reactive_Programming.md)

* **Core Concept**: Library for composing asynchronous, event-driven programs using observable streams and functional transformation operators.
* **Real-World Analogy**: An **Assembly Conveyor Belt**. Items travel down the belt; sorting arms divert, filter, debounce, and pack items into boxes before final delivery.
* **Key Takeaways & Interview Gotchas**:
  * **Subject Types**:
    * `Subject`: Multicast; emits only values arriving *after* subscription.
    * `BehaviorSubject`: Stores the latest value; requires initial value; emits immediately to new subscribers.
    * `ReplaySubject`: Buffers a specified number of past values for new subscribers.
  * **Flattening Operators Comparison**:
    * `switchMap`: **Cancels previous inner observable** when a new value arrives (Ideal for search/typeaheads).
    * `mergeMap`: Runs all inner observables **concurrently** (Ideal for parallel tasks).
    * `concatMap`: Queues inner observables and executes them **sequentially** in order.
    * `exhaustMap`: **Ignores new values** while the current inner observable is running (Ideal for submit buttons).
  * **Clean Unsubscribing**: Use `takeUntilDestroyed()` (from `@angular/core/rxjs-interop`) or `AsyncPipe` to prevent memory leaks.

```typescript
// Search Typeahead Implementation
import { Component, inject } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { debounceTime, distinctUntilChanged, switchMap } from 'rxjs/operators';
import { AsyncPipe } from '@angular/common';

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [ReactiveFormsModule, AsyncPipe],
  template: `
    <input [formControl]="searchControl" placeholder="Search products..." />
    <ul>
      @for (item of searchResults$ | async; track item.id) {
        <li>{{ item.name }}</li>
      }
    </ul>
  `
})
export class SearchComponent {
  private http = inject(HttpClient);
  searchControl = new FormControl('');

  searchResults$ = this.searchControl.valueChanges.pipe(
    debounceTime(300),                         // Wait 300ms pause in typing
    distinctUntilChanged(),                    // Ignore identical queries
    switchMap(query => this.http.get<any[]>(`/api/search?q=${query}`)) // Cancel old request
  );
}
```

---

## 18. State Management
🔗 **Full Lesson:** [18_State_Management.md](./18_State_Management.md)

* **Core Concept**: Manages application state as a single source of truth across all components to eliminate data inconsistency and state scattering.
* **Real-World Analogy**: A **Company Ledger**. To prevent accounting discrepancies, only designated accountants (Reducers) can update accounts using official transaction slips (Actions).
* **Key Takeaways & Interview Gotchas**:
  * **When to use what**:
    * **Signals / Service Store**: Perfect for small to medium apps (low complexity, zero boilerplate).
    * **NgRx (Redux pattern)**: Ideal for large enterprise apps with high data complexity and multi-team collaboration.
  * **NgRx Core Pillars**:
    1. **Actions**: Plain objects describing what event happened (e.g., `[Cart] Add Item`).
    2. **Reducers**: Pure functions computing the new state from `(previousState, action)`.
    3. **Selectors**: Memoized queries extracting specific slices of state.
    4. **Effects**: Handles asynchronous side-effects (API data fetching).

```typescript
// Simple Signal-Based State Store Pattern
import { Injectable, signal, computed } from '@angular/core';

interface AppState { user: string | null; theme: 'dark' | 'light'; }

@Injectable({ providedIn: 'root' })
export class AppStore {
  private state = signal<AppState>({ user: null, theme: 'light' });

  // Selectors
  user = computed(() => this.state().user);
  theme = computed(() => this.state().theme);

  // Actions
  setUser(user: string) { this.state.update(s => ({ ...s, user })); }
  toggleTheme() { this.state.update(s => ({ ...s, theme: s.theme === 'light' ? 'dark' : 'light' })); }
}
```

---

## 19. Authentication and Authorization
🔗 **Full Lesson:** [19_Authentication_and_Authorization.md](./19_Authentication_and_Authorization.md)

* **Core Concept**: Secures client routes and backend API requests by managing JSON Web Tokens (Access & Refresh Tokens), route authorization guards, and automated token renewal.
* **Real-World Analogy**: **Theme Park Wristbands**. Your entry wristband (Access Token) grants access to ride zones; when it expires, you show your receipt (Refresh Token) at customer service to receive a new wristband without having to re-authenticate at the entrance.
* **Key Takeaways & Interview Gotchas**:
  * **JWT Storage**: Store tokens in secure memory, secure HTTP-only cookies, or encrypted local storage.
  * **Refresh Token Interceptor Strategy**: Intercept `401 Unauthorized` responses, pause pending requests, call the refresh token endpoint, and replay failed requests with the new token.

```typescript
// 401 Refresh Token Handling Pattern
import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, switchMap, throwError } from 'rxjs';
import { AuthService } from './auth.service';

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const auth = inject(AuthService);

  return next(req).pipe(
    catchError((err: HttpErrorResponse) => {
      if (err.status === 401 && !req.url.includes('/auth/refresh')) {
        return auth.refreshToken().pipe(
          switchMap(newToken => {
            return next(req.clone({ setHeaders: { Authorization: `Bearer ${newToken}` } }));
          })
        );
      }
      return throwError(() => err);
    })
  );
};
```

---

## 20. Angular Material
🔗 **Full Lesson:** [20_Angular_Material.md](./20_Angular_Material.md)

* **Core Concept**: Google's official UI component library for Angular implementing Material Design principles, built-in accessibility (a11y), and responsive layout components.
* **Real-World Analogy**: **Modular Architectural Panels**. Instead of hand-molding individual bricks, you assemble modular, pre-fabricated panels with built-in accessibility ramps and electrical sockets.
* **Key Takeaways & Interview Gotchas**:
  * **Standalone Integration**: Import only the specific component modules required (e.g., `MatButtonModule`, `MatTableModule`, `MatDialogModule`).
  * **Angular CDK (Component Development Kit)**: Provides headless utilities including Drag & Drop (`@angular/cdk/drag-drop`), Virtual Scrolling (`@angular/cdk/scrolling`), and Overlays.

```typescript
import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-mat-demo',
  standalone: true,
  imports: [MatButtonModule, MatCardModule],
  template: `
    <mat-card>
      <mat-card-title>Angular Material Card</mat-card-title>
      <mat-card-actions>
        <button mat-raised-button color="primary">Confirm</button>
      </mat-card-actions>
    </mat-card>
  `
})
export class MatDemoComponent {}
```

---

## 21. Performance Optimization
🔗 **Full Lesson:** [21_Performance_Optimization.md](./21_Performance_Optimization.md)

* **Core Concept**: Techniques to minimize initial page load time, bundle size, and runtime Change Detection overhead.
* **Real-World Analogy**: **Security Checkpoints**. Skipping security checks on houses until their door alarm is specifically triggered (`OnPush` change detection strategy).
* **Key Takeaways & Interview Gotchas**:
  * **`ChangeDetectionStrategy.OnPush`**: Checks component view only when an `@Input()` reference changes or an event originates inside the component.
  * **`@defer` Block**: Lazy loads heavy components when they enter the viewport (`on viewport`), on user interaction (`on interaction`), or on browser idle (`on idle`).
  * **Track in `@for`**: Always specify a unique identity key (e.g., `track item.id`) to prevent unnecessary DOM destruction and re-creation.
  * **`NgOptimizedImage` (`ngSrc`)**: Enforces responsive image sizing, prevents layout shifts (CLS), and automatically sets priority preloading.

```typescript
@Component({
  selector: 'app-perf-item',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush // Skips unnecessary checks
})
export class PerfItemComponent {
  @Input() itemData!: any;
}
```

```html
<!-- Defer heavy chart component until scrolled into viewport -->
@defer (on viewport) {
  <app-heavy-chart [data]="chartData" />
} @placeholder {
  <div class="skeleton-loader">Loading Chart...</div>
}
```

---

## 22. Testing (Jasmine & Jest)
🔗 **Full Lesson:** [22_Testing_Jasmine_Jest.md](./22_Testing_Jasmine_Jest.md)

* **Core Concept**: Validates component and service behavior through automated unit and integration tests using `TestBed`.
* **Real-World Analogy**: **Flight Simulators**. Testing airplane flight control responses under simulated storm conditions before carrying real passengers.
* **Key Takeaways & Interview Gotchas**:
  * **`TestBed`**: Angular's test harness for configuring mock dependencies and creating component instances (`ComponentFixture`).
  * **`HttpTestingController`**: Mocks backend HTTP requests and verifies URL endpoints (`expectOne()`) and payload responses (`req.flush()`).
  * **`fixture.detectChanges()`**: Manually triggers Change Detection in test environments.

```typescript
// Component Unit Test Example
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CounterComponent } from './counter.component';

describe('CounterComponent', () => {
  let component: CounterComponent;
  let fixture: ComponentFixture<CounterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CounterComponent] // Standalone component
    }).compileComponents();

    fixture = TestBed.createComponent(CounterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should increment count when increment() is called', () => {
    expect(component.count()).toBe(0);
    component.increment();
    expect(component.count()).toBe(1);
  });
});
```

---

## 23. Security Best Practices
🔗 **Full Lesson:** [23_Security_Best_Practices.md](./23_Security_Best_Practices.md)

* **Core Concept**: Protecting applications against Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF), and unauthorized data leaks.
* **Real-World Analogy**: A **Hazardous Materials Mailroom**. All incoming mail is automatically sterilized. Bypassing sterilization requires an explicit security badge override from senior management.
* **Key Takeaways & Interview Gotchas**:
  * **Built-in Sanitization**: Angular treats all untrusted values as dangerous by default and automatically sanitizes HTML/CSS/URLs in template bindings.
  * **`DomSanitizer`**: Use `bypassSecurityTrustHtml` or `bypassSecurityTrustResourceUrl` **only** when content has been strictly validated from safe internal sources.
  * **Direct DOM Avoidance**: Never use native `element.innerHTML` or `document.getElementById()`; always use Angular template bindings or `Renderer2`.

```typescript
import { Component, inject } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({ selector: 'app-security', standalone: true, template: `<iframe [src]="safeUrl"></iframe>` })
export class SecurityComponent {
  private sanitizer = inject(DomSanitizer);
  // Warning: Only bypass on verified, trusted URLs!
  safeUrl: SafeResourceUrl = this.sanitizer.bypassSecurityTrustResourceUrl('https://trusted-domain.com');
}
```

---

## 24. SSR and Advanced Concepts
🔗 **Full Lesson:** [24_SSR_and_Advanced_Concepts.md](./24_SSR_and_Advanced_Concepts.md)

* **Core Concept**: Server-Side Rendering (`@angular/ssr`) renders Angular HTML on a Node.js server before sending it to the client, improving initial page load (FCP) and Search Engine Optimization (SEO).
* **Real-World Analogy**: **Meal Prepping**. Cooking and packing complete meals at a central kitchen (SSR Server) so clients only have to warm them up (Client Hydration) upon arrival.
* **Key Takeaways & Interview Gotchas**:
  * **Non-Destructive Hydration**: Modern Angular hydrates the pre-rendered server DOM without destroying and re-rendering HTML nodes, eliminating visual screen flickers.
  * **Platform Checks**: Guard browser-only globals (`window`, `localStorage`, `document`) using `isPlatformBrowser(platformId)` to prevent Node.js server crashes.
  * **Event Replay**: Records user clicks/events during SSR page loading and automatically replays them after client hydration completes.

```typescript
import { Component, inject, PLATFORM_ID, OnInit } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

@Component({ selector: 'app-ssr-demo', standalone: true, template: `<p>SSR Component</p>` })
export class SsrDemoComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      // Safe to access browser APIs
      console.log('Current URL:', window.location.href);
    }
  }
}
```

---

## 25. Enterprise Architecture
🔗 **Full Lesson:** [25_Enterprise_Architecture.md](./25_Enterprise_Architecture.md)

* **Core Concept**: Structuring large codebases into scalable, decoupled layers (Smart vs. Dumb components, Feature vs. Shared modules) to enable multiple teams to work in parallel.
* **Real-World Analogy**: **Military Command Structure**. HQ officers decide battle strategies and coordinate logistics (Smart / Container Components), while front-line squads execute specific tasks with the tools provided (Dumb / Presentational Components).
* **Key Takeaways & Interview Gotchas**:
  * **Smart (Container) Components**: Inject services, handle routing, manage state streams, and pass data down to children.
  * **Dumb (Presentational) Components**: Pure UI widgets; accept data via `@Input()` / `input()`, emit actions via `@Output()` / `output()`, and contain zero HTTP or state dependencies.
  * **Recommended Directory Structure**:
    * `core/`: Global singletons, auth interceptors, root guards.
    * `shared/`: Reusable dumb UI components, custom pipes, directives.
    * `features/`: Domain-specific business modules (e.g., `features/billing`, `features/orders`).

```
src/app/
 ├── core/              # Singletons, auth guards, interceptors
 ├── shared/            # Reusable UI widgets, pipes, directives
 └── features/          # Domain feature pages
      ├── auth/
      ├── billing/
      └── dashboard/
```

---

## 26. Deployment and CI/CD
🔗 **Full Lesson:** [26_Deployment_and_CI_CD.md](./26_Deployment_and_CI_CD.md)

* **Core Concept**: Automating compilation, linting, testing, Docker containerization, and static web server hosting for production deployments.
* **Real-World Analogy**: An **Automated Shipping Logistics Center**. Inspects item quality, packages bundles into standardized containers, and ships them to global distribution hubs automatically.
* **Key Takeaways & Interview Gotchas**:
  * **SPA Fallback Routing**: In Nginx/Apache, client-side routing requires rewriting all requests to `/index.html` via `try_files $uri $uri/ /index.html;` so deep links don't return 404 errors.
  * **Multi-Stage Docker Build**: Build the app in a Node environment stage, then copy only the compiled `/dist` files into a lightweight Nginx alpine image.

```dockerfile
# Multi-Stage Dockerfile
# Stage 1: Build Angular App
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build -- --configuration production

# Stage 2: Serve via Nginx
FROM nginx:alpine
COPY --from=build /app/dist/my-app/browser /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

```nginx
# nginx.conf - SPA Fallback
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        # Redirect all requests to index.html for Angular client-side router
        try_files $uri $uri/ /index.html;
    }
}
```

---

Previous : [00_index.md](./00_index.md) | Index : [00_index.md](./00_index.md) | Next : [01_Introduction_to_Angular.md](./01_Introduction_to_Angular.md)
