# 🅰️ Angular – Complete Revision Guide

Welcome to the Angular master module revision sheet. This document aggregates all key architectural concepts, configuration commands, typescript syntax, design analogies, production best practices, and interview-prep notes from every topic in this directory, allowing you to perform a complete revision of Angular from a single index file.

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
- [27. Real World E-Commerce Project](#27-real-world-e-commerce-project)
- [28. Beginner Interview Prep](#28-beginner-interview-prep)
- [29. Interview Prep - Intermediate](#29-interview-prep---intermediate)
- [30. Interview Prep - Advanced](#30-interview-prep---advanced)
- [31. Scenario and System Design](#31-scenario-and-system-design)

---

## 01. Introduction to Angular
🔗 **Full Lesson:** [01_Introduction_to_Angular.md](./01_Introduction_to_Angular.md)

* **Why It Exists**: Enforces structural standardizations across enterprise codebases. Bypasses the need to cobble together router, state, and compiler libraries manually.
* **Real-World Analogy**: A pre-furnished **Custom Smart Home**. It comes with structural plumbing (DI), wiring (Router), and thermostat controls (HttpClient) already integrated. You only add decorations (Components).
* **Architecture Difference (vs. React/Vue)**:
  * **React**: A library focusing on UI rendering; leaves architecture decisions (routing, forms, state) to external packages.
  * **Angular**: A fully-integrated enterprise framework providing all parts (DI, forms, routing, testing, HTTP client) out-of-the-box. Enforces TypeScript.

### Conceptual Comparison:
```
React Flow:   DOM Updates ──> Virtual DOM Diffing ──> Re-render Component Tree
Angular Flow: Change Detection ──> Zone.js (or Zoneless Signals) ──> Directly update specific DOM node
```

---

## 02. Setup and Environment
🔗 **Full Lesson:** [02_Setup_and_Environment.md](./02_Setup_and_Environment.md)

* **Why It Exists**: Automates code scaffolding, testing environments, and optimized build compilations (tree-shaking and minification) locally and in CI/CD.
* **Real-World Analogy**: An **Automated Factory Assembly Line**. Instead of hand-carving gears (creating files manually), you run a control panel (CLI) to output pre-tested gears directly into the chassis.

### Key CLI Commands:
```bash
npm install -g @angular/cli                              # Install Angular CLI globally
ng new my-app --standalone --style=css                   # Generate new standalone application
ng serve --port 4200 --open                              # Run local development server
ng generate component components/user-profile            # Scaffolds UserProfile component files
ng generate service services/auth                        # Scaffolds AuthService file and tests
ng build --configuration production                      # Compile optimized production bundles
```

---

## 03. TypeScript Fundamentals
🔗 **Full Lesson:** [03_Typescript_Fundamentals.md](./03_Typescript_Fundamentals.md)

* **Why It Exists**: Captures data mismatches, null values, and contract breaking at compile-time before code gets deployed to users.
* **Real-World Analogy**: **Construction Blueprints**. Checking blueprint specifications before pouring concrete avoids realizing later that the support pillars are misaligned.

### Key Syntax Configurations:
```typescript
interface User { id: string; name: string; email: string; role: 'admin' | 'user' }
type Response<T> = { data: T; status: number; error?: string };

// Generics and Union Types in Action
function getUserData<T>(userId: string): Promise<Response<T>> {
  return fetch(`/api/users/${userId}`).then(res => res.json());
}
```

> [!IMPORTANT]
> **Interface vs Type**: Use `interface` for declaring public API structures and classes (due to declaration merging and OOP extensibility). Use `type` for complex unions, tuples, or utility types.

---

## 04. Angular Architecture
🔗 **Full Lesson:** [04_Angular_Architecture.md](./04_Angular_Architecture.md)

* **Why It Exists**: Replaces modular code bundling (`NgModule`) with standalone component structures to reduce boilerplate and improve tree-shaking performance.
* **Real-World Analogy**: A **Self-Sufficient Smart Village**. Instead of a central electricity station distributing utility configurations (NgModule), each house has its own solar panels and battery backup systems (Standalone components declaring imports).

### Bootstrapping Flow:
```typescript
// main.ts
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));
```

---

## 05. Components and Templates
🔗 **Full Lesson:** [05_Components_and_Templates.md](./05_Components_and_Templates.md)

* **Why It Exists**: Unifies presentation markup (HTML) and UI logic (TS class) into reusable, self-contained view modules.
* **Real-World Analogy**: **Vehicle Instrument Panel**. The engine controller (TS class) updates speed displays (Property Binding) and registers driver dial adjustment events (Event Binding) synchronously.

### Binding Syntax:
```html
<h2>Welcome, {{ username }}</h2>                         <!-- Interpolation -->
<img [src]="profileImageUrl" alt="Avatar">              <!-- Property Binding -->
<button (click)="onLogout()">Log Out</button>            <!-- Event Binding -->
<input [(ngModel)]="searchQuery" placeholder="Search">   <!-- Two-Way Binding (Forms) -->
<div #containerElement>Container Box</div>               <!-- Template Reference Variable -->
```

---

## 06. Pipes
🔗 **Full Lesson:** [06_Pipes.md](./06_Pipes.md)

* **Why It Exists**: Formats raw variables in templates on-the-fly without polluting component controllers with formatting logic.
* **Real-World Analogy**: **Water Filtration Nozzles**. Raw water enters the hose; different nozzles output mist, stream, or spray options without changing the source water supply.

### Pure vs Impure Pipes:
* **Pure Pipe (Default)**: Executes only when reference checks change (highly performant, uses cached calculations).
* **Impure Pipe**: Executes on every change detection cycle (can create performance issues if doing heavy tasks).

### Key Pipes Syntax:
```html
<p>{{ price | currency:'EUR' }}</p>                       <!-- Built-in currency pipe -->
<p>{{ today | date:'yyyy-MM-dd' }}</p>                    <!-- Date pipe -->
<p>{{ userData$ | async }}</p>                            <!-- Async Pipe (Auto-unsubscribe) -->
```

---

## 07. Directives
🔗 **Full Lesson:** [07_Directives.md](./07_Directives.md)

* **Why It Exists**: Attaches custom interactive behaviors (Attribute) or conditionally restructures the DOM layout (Structural) directly in elements.
* **Real-World Analogy**: **Wearable Sensor Badges**. Pinning a badge to a worker triggers notifications when they enter unauthorized zones without modifying the worker's attributes.

### Attribute Directives and Host Decorators:
```typescript
@Directive({ selector: '[appHoverHighlight]', standalone: true })
export class HoverHighlightDirective {
  @HostBinding('style.backgroundColor') bgColor = 'transparent';
  @HostListener('mouseenter') onMouseEnter() { this.bgColor = 'yellow'; }
  @HostListener('mouseleave') onMouseLeave() { this.bgColor = 'transparent'; }
}
```

---

## 08. Component Lifecycle
🔗 **Full Lesson:** [08_Component_Lifecycle.md](./08_Component_Lifecycle.md)

* **Why It Exists**: Hooks developers into key runtime moments (initialization, change updates, and destruction) to execute async calls and cleanup tasks.
* **Real-World Analogy**: **Theatrical Play Stages**. Setup lighting (ngOnInit), adjust scripts when actors speak (ngOnChanges), check positions (ngAfterViewInit), and strike the set at the end of the show (ngOnDestroy).

### Lifecycle Order:
1. `Constructor`: Class instantiated (never place API calls here).
2. `ngOnChanges`: Triggered when `@Input` variables change references.
3. `ngOnInit`: Component initialization (fetch data here).
4. `ngDoCheck`: Custom check handler.
5. `ngAfterViewInit`: HTML child template DOM queries fully initialized.
6. `ngOnDestroy`: Cleanup phase (unsubscribe from streams, destroy timers).

---

## 09. Component Communication
🔗 **Full Lesson:** [09_Component_Communication.md](./09_Component_Communication.md)

* **Why It Exists**: Coordinates data sharing, UI events, and structural templating across nested parent-child component boundaries.
* **Real-World Analogy**: **Office Walkie-Talkies**. Parent managers broadcast tasks down (Inputs), and worker components report back via alert pings (Outputs).

### Communication Syntax:
```typescript
// Child Component
export class ChildComponent {
  @Input() userData!: User;
  @Output() statusChanged = new EventEmitter<string>();
  
  triggerUpdate() { this.statusChanged.emit('COMPLETED'); }
}
```
```html
<!-- Parent Template -->
<app-child [userData]="selectedUser" (statusChanged)="onStatusChange($event)"></app-child>
```

---

## 10. Signals
🔗 **Full Lesson:** [10_Signals.md](./10_Signals.md)

* **Why It Exists**: Introduces fine-grained reactivity to track status reads. Only updates DOM elements affected by change, bypassing Zone.js dirty-checking overhead.
* **Real-World Analogy**: **Spreadsheet Cells**. Changing value in cell `A1` immediately updates cell `C1` via formula without checking every other cell in the file.

### Signals Syntax:
```typescript
const count = signal(0);                                  // Writable Signal
const doubleCount = computed(() => count() * 2);          // Computed Signal (Cached)
effect(() => console.log(`Count changed to: ${count()}`)); // Effect (runs on changes)

count.set(5);                                             // Direct value write
count.update(val => val + 1);                             // Calculate new state
```

---

## 11. Dependency Injection
🔗 **Full Lesson:** [11_Dependency_Injection.md](./11_Dependency_Injection.md)

* **Why It Exists**: Decouples component logic from instance creations, enabling test mocking and centralizing service instances.
* **Real-World Analogy**: A **Central Supply Closet**. Instead of every builder manufacturing their own drill (instantiating new services), they ask the supplier (DI Injector) to supply one.

### DI Providers Configuration:
```typescript
// Service Registration
@Injectable({ providedIn: 'root' })                       // Register globally (Singleton)
export class NetworkService {}

// Component Consumer
export class Component {
  constructor(private network: NetworkService) {}         // Inject service via constructor
}
```

---

## 12. Services and Business Logic
🔗 **Full Lesson:** [12_Services_and_Business_Logic.md](./12_Services_and_Business_Logic.md)

* **Why It Exists**: Prevents UI components from bloating by separating computational state, data mapping, and API networking logic.
* **Real-World Analogy**: **Restaurant Waiter & Kitchen**. The waiter (Component) only takes orders and serves plates; the kitchen (Service) handles sourcing ingredients, cooking, and plating.

### Code Pattern:
```typescript
@Injectable({ providedIn: 'root' })
export class CartService {
  private cartItems = signal<Product[]>([]);
  public items = this.cartItems.asReadonly();

  addToCart(product: Product) {
    this.cartItems.update(current => [...current, product]);
  }
}
```

---

## 13. Routing and Navigation
🔗 **Full Lesson:** [13_Routing_and_Navigation.md](./13_Routing_and_Navigation.md)

* **Why It Exists**: Dynamically switches page views in client code based on browser URL configurations, preventing full page reloads.
* **Real-World Analogy**: **Airport Terminals**. The central runway stays fixed; paths route passengers to different gates (components) depending on their boarding tickets.

### Route Configs & Functional Guards:
```typescript
export const routes: Routes = [
  { path: 'dashboard', loadComponent: () => import('./dashboard.component').then(c => c.DashboardComponent), canActivate: [authGuard] },
  { path: 'users/:id', component: UserDetailComponent }
];

export const authGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  return inject(AuthService).isLoggedIn() ? true : router.createUrlTree(['/login']);
};
```

---

## 14. Template-Driven Forms
🔗 **Full Lesson:** [14_Template_Driven_Forms.md](./14_Template_Driven_Forms.md)

* **Why It Exists**: Quick, declarative form creation using directive bindings in HTML templates.
* **Real-World Analogy**: **Paper Questionnaires**. Fill in inputs directly on the sheet; the formatting and fields are predefined on paper.

### Form Bindings Template:
```html
<form #loginForm="ngForm" (ngSubmit)="onSubmit(loginForm.value)">
  <input name="email" ngModel required email #emailInput="ngModel">
  @if (emailInput.invalid && emailInput.touched) { <span class="error">Enter email</span> }
  <button type="submit" [disabled]="loginForm.invalid">Submit</button>
</form>
```

---

## 15. Reactive Forms
🔗 **Full Lesson:** [15_Reactive_Forms.md](./15_Reactive_Forms.md)

* **Why It Exists**: Provides a programmatic, type-safe API to build, validate, dynamic-track, and test complex form fields inside class files.
* **Real-World Analogy**: **Programmatic Spreadsheets**. Creating validation constraints cell-by-cell in code, checking input values, and calculating rules in real-time.

### Forms Control Configurations:
```typescript
export class FormComponent {
  private fb = inject(FormBuilder);
  loginForm = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]]
  });

  submit() {
    if (this.loginForm.valid) { console.log(this.loginForm.value); }
  }
}
```

---

## 16. HttpClient and API Integration
🔗 **Full Lesson:** [16_HttpClient_and_API_Integration.md](./16_HttpClient_and_API_Integration.md)

* **Why It Exists**: Handles backend networking requests, automatically parses JSON payloads, and handles headers/tokens globally.
* **Real-World Analogy**: **Registered Shipping Clerk**. Attaches custom delivery stamps (Auth headers) and signs off confirmations before letters leave the building.

### Functional Interceptor and Request Call:
```typescript
// Functional Interceptor
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authToken = inject(AuthService).getToken();
  const authReq = req.clone({ setHeaders: { Authorization: `Bearer ${authToken}` } });
  return next(authReq);
};
```

---

## 17. RxJS Reactive Programming
🔗 **Full Lesson:** [17_RxJS_Reactive_Programming.md](./17_RxJS_Reactive_Programming.md)

* **Why It Exists**: Manages complex asynchronous event streams, timeouts, and API dependencies using a functional programming paradigm.
* **Real-World Analogy**: **Assembly Conveyor Belt**. Diverts, aggregates, and transforms items along the belt (using operators) before boxing them.

### Key Operators Example:
```typescript
import { debounceTime, distinctUntilChanged, switchMap } from 'rxjs/operators';

searchTerms$.pipe(
  debounceTime(300),                                      // Wait for 300ms pause
  distinctUntilChanged(),                                 // Ignore duplicate sequential entries
  switchMap(term => this.api.search(term))                // Cancel old request, switch to new query stream
).subscribe(results => this.displayResults(results));
```

---

## 18. State Management
🔗 **Full Lesson:** [18_State_Management.md](./18_State_Management.md)

* **Why It Exists**: Prevents state scattering by maintaining a predictable single source of truth across enterprise layouts.
* **Real-World Analogy**: **Company Ledger**. Only accountants (Reducers) can update accounts using transaction slips (Actions) to prevent database discrepancies.

### Store Architecture:
* **Actions**: Describe the event (e.g. `[Cart] Add Item`).
* **Reducers**: Pure functions calculating the new state based on actions.
* **Selectors**: Queries used to fetch specific fields from the state tree.
* **Effects**: Asynchronous side-effects (e.g. fetching API data).

---

## 19. Authentication and Authorization
🔗 **Full Lesson:** [19_Authentication_and_Authorization.md](./19_Authentication_and_Authorization.md)

* **Why It Exists**: Secures client routes and API requests by managing tokens, expiry validation checks, and role mappings.
* **Real-World Analogy**: **Theme Park Passes**. Wristbands (Tokens) grant access to ride zones; expired passes are automatically renewed at ticket booths (Refresh Tokens).

### Refresh Token Interceptor Strategy:
```typescript
// Pseudo-code for handling expired tokens on 401 response
return next(req).pipe(
  catchError((error) => {
    if (error instanceof HttpErrorResponse && error.status === 401) {
      return this.auth.refreshToken().pipe(
        switchMap((newToken) => next(req.clone({ setHeaders: { Authorization: `Bearer ${newToken}` } })))
      );
    }
    return throwError(() => error);
  })
);
```

---

## 20. Angular Material
🔗 **Full Lesson:** [20_Angular_Material.md](./20_Angular_Material.md)

* **Why It Exists**: Standardizes application UIs using ready-made material design components (Data Tables, Dialogs, Inputs).
* **Real-World Analogy**: **Modular Building Blocks**. Instead of baking custom bricks, you assemble modular panels with built-in accessibility.

### Component Usage Configuration:
```typescript
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';

@Component({
  standalone: true,
  imports: [MatButtonModule, MatTableModule],
  template: `<button mat-raised-button color="primary">Submit</button>`
})
export class MaterialComponent {}
```

---

## 21. Performance Optimization
🔗 **Full Lesson:** [21_Performance_Optimization.md](./21_Performance_Optimization.md)

* **Why It Exists**: Reduces initial page load times and optimizes runtime execution speeds (change detection cycles).
* **Real-World Analogy**: **Security Checkpoints**. Skip checks on houses unless their gate alarm is tripped (OnPush change detection strategy).

### Optimization Strategy configurations:
```typescript
@Component({
  selector: 'app-perf-item',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush          // Skips checks unless input reference changes
})
export class PerfItemComponent {
  @Input() data!: ItemData;
}
```
```html
<!-- Defer block to lazy load heavy component when it enters viewport -->
@defer (on viewport) {
  <app-heavy-chart></app-heavy-chart>
} @placeholder {
  <div>Loading Chart...</div>
}
```

---

## 22. Testing (Jasmine & Jest)
🔗 **Full Lesson:** [22_Testing_Jasmine_Jest.md](./22_Testing_Jasmine_Jest.md)

* **Why It Exists**: Ensures code quality and prevents regression bugs when writing changes or upgrading libraries.
* **Real-World Analogy**: **Flight Simulator**. Test cockpit responses under different conditions before flying actual passengers.

### Key TestBed Setup:
```typescript
describe('UserService Spec', () => {
  let service: UserService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [UserService, provideHttpClient(), provideHttpClientTesting()]
    });
    service = TestBed.inject(UserService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('should fetch users', () => {
    service.getUsers().subscribe(users => expect(users.length).toBe(2));
    const req = httpMock.expectOne('/api/users');
    req.flush([{ id: 1 }, { id: 2 }]);
  });
});
```

---

## 23. Security Best Practices
🔗 **Full Lesson:** [23_Security_Best_Practices.md](./23_Security_Best_Practices.md)

* **Why It Exists**: Defends applications from malicious script injections (XSS) and request hijackings (CSRF).
* **Real-World Analogy**: **Mailroom Sterilizer**. Mail is automatically sanitized before delivery. Bypass options require manager override.

### Sanitizer Implementation:
```typescript
export class SecurityComponent {
  private sanitizer = inject(DomSanitizer);
  
  // Safe bypass syntax. Warn: Only use with verified inputs!
  trustedUrl = this.sanitizer.bypassSecurityTrustResourceUrl('https://trusted-partner.com');
}
```

---

## 24. SSR and Advanced Concepts
🔗 **Full Lesson:** [24_SSR_and_Advanced_Concepts.md](./24_SSR_and_Advanced_Concepts.md)

* **Why It Exists**: Pre-renders templates on Node.js servers to support crawler indices (SEO) and reduce initial render delays.
* **Real-World Analogy**: **Meal Prepping**. Cook the food in a central kitchen (SSR server) and package it, so clients only need to heat it up (Hydration).

### Platform Check Configs:
```typescript
import { isPlatformBrowser } from '@angular/common';
import { PLATFORM_ID } from '@angular/core';

export class AdvancedComponent {
  private platformId = inject(PLATFORM_ID);

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      // Safe to call window or document API here
      console.log(window.location.href);
    }
  }
}
```

---

## 25. Enterprise Architecture
🔗 **Full Lesson:** [25_Enterprise_Architecture.md](./25_Enterprise_Architecture.md)

* **Why It Exists**: Divides code bases into feature domains, decoupling infrastructure, services, and smart vs dumb UI boundaries.
* **Real-World Analogy**: **Military Command Structure**. Command towers decide maneuvers (Smart Components), while front-line squads execute commands (Dumb Components).

### Smart Component (Container) vs Dumb Component (Presentation):
* **Smart**: Injects services, manages state streams, coordinates network APIs.
* **Dumb**: Reusable UI blocks, accepts data via `@Input`, emits user events via `@Output`.

---

## 26. Deployment and CI/CD
🔗 **Full Lesson:** [26_Deployment_and_CI_CD.md](./26_Deployment_and_CI_CD.md)

* **Why It Exists**: Automates build pipelines, formats stylesheets, runs test suites, and pushes compiled files to server environments.
* **Real-World Analogy**: **Manufacturing Shipping Center**. Quality check, pack boxes, stamp addresses, and load shipping containers automatically.

### Production Nginx Routing Configuration (`nginx.conf`):
```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        # Redirect all requests to index.html to support client-side routing
        try_files $uri $uri/ /index.html;
    }
}
```

---

## 27. Real World E-Commerce Project
🔗 **Full Lesson:** [27_Real_World_ECommerce_Project.md](./27_Real_World_ECommerce_Project.md)

* **Why It Exists**: Practical integration of lazy-loaded routes, state stores, secure authentication, API interceptors, and checkout paths in a unified project.
* **Real-World Analogy**: **Online Mall**. Integrates display shelves (catalog feature), user accounts (auth feature), cashiers (payment feature), and shopping carts (state feature).

---

## 28. Beginner Interview Prep
🔗 **Full Lesson:** [28_Interview_Prep_Beginner.md](./28_Interview_Prep_Beginner.md)

* **Scope**: Evaluates knowledge of basic directive syntax, TypeScript bindings, and setup workflows.
* **Example Question**: *What is the difference between `@Input` and `@Output`?*
  * **Answer**: `@Input` passes data down from parent components to child components. `@Output` uses `EventEmitter` to bubble up action events from children to parents.

---

## 29. Interview Prep - Intermediate
🔗 **Full Lesson:** [29_Interview_Prep_Intermediate.md](./29_Interview_Prep_Intermediate.md)

* **Scope**: Evaluates knowledge of reactive form schemas, custom validation, pipes, directives, and lifecycle hooks.
* **Example Question**: *What is the difference between Reactive Forms and Template-Driven Forms?*
  * **Answer**: Template-driven forms use declarative directives (like `ngModel`) in the HTML template (easier, relies on two-way bindings). Reactive forms are declared programmatically in the TypeScript class (type-safe, scalable, testable, runs via RxJS streams).

---

## 30. Interview Prep - Advanced
🔗 **Full Lesson:** [30_Interview_Prep_Advanced.md](./30_Interview_Prep_Advanced.md)

* **Scope**: Evaluates custom DI providers, performance, change detection, complex RxJS operators, and token refresh interceptors.
* **Example Question**: *Explain how OnPush change detection improves performance.*
  * **Answer**: By default, change detection traverses the entire component tree. `OnPush` tells Angular to skip checking a component and its children unless its `@Input` property references update, a component event fires, or change detection is triggered manually.

---

## 31. Scenario and System Design
🔗 **Full Lesson:** [31_Interview_Prep_Scenario_and_System_Design.md](./31_Interview_Prep_Scenario_and_System_Design.md)

* **Scope**: Enterprise systems architecture, monorepos, state management boundaries, caching interceptors, and SSR hydration.
* **Example Question**: *How do you build a caching HTTP interceptor in Angular?*
  * **Answer**: Use a Map cache. The interceptor intercepts outgoing `GET` requests, checks if the URL exists in the map cache, and if so, returns a cached `HttpResponse` observable. If it does not exist, it executes the network call, saves the response in the map cache, and sets an expiration timer.

---
Previous : [00_index.md](./00_index.md) | Index : [00_index.md](./00_index.md) | Next : [01_Introduction_to_Angular.md](./01_Introduction_to_Angular.md)
