# 🅰️ Angular – Complete Revision Guide

Welcome to the Angular master module revision sheet. Is document me saare key architectural concepts, configuration commands, typescript syntax, design analogies, production best practices, aur interview-prep notes ko is directory ke har topic se aggregate kiya gaya hai, taaki aap ek single index file se Angular ka complete revision kar sakein.

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

* **Why It Exists (Yeh kyun exist karta hai)**: Enterprise codebases me structural standardizations ko enforce karta hai. Router, state, aur compiler libraries ko manually aapas me jodne (cobble together) ki zaroorat ko khatam karta hai.
* **Real-World Analogy (Real-world Udaharan)**: Ek pre-furnished **Custom Smart Home**. Yeh structural plumbing (DI), wiring (Router), aur thermostat controls (HttpClient) ke sath pehle se hi integrated aata hai. Aapko sirf isme decorations (Components) add karne hote hain.
* **Architecture Difference (vs. React/Vue) (Architecture me Difference)**:
  * **React**: Ek library hai jo UI rendering par focus karti hai; architectural decisions (routing, forms, state) ko external packages par chodh deti hai.
  * **Angular**: Ek fully-integrated enterprise framework hai jo saare parts (DI, forms, routing, testing, HTTP client) out-of-the-box provide karta hai. Yeh TypeScript ko enforce karta hai.

### Conceptual Comparison:
```
React Flow:   DOM Updates ──> Virtual DOM Diffing ──> Re-render Component Tree
Angular Flow: Change Detection ──> Zone.js (or Zoneless Signals) ──> Directly update specific DOM node
```

---

## 02. Setup and Environment
🔗 **Full Lesson:** [02_Setup_and_Environment.md](./02_Setup_and_Environment.md)

* **Why It Exists (Yeh kyun exist karta hai)**: Local aur CI/CD me code scaffolding, testing environments, aur optimized build compilations (tree-shaking aur minification) ko automate karta hai.
* **Real-World Analogy (Real-world Udaharan)**: Ek **Automated Factory Assembly Line**. Manually gears generate karne (files manually create karne) ke bajaye, aap ek control panel (CLI) run karte hain taaki pre-tested gears directly chassis me output ho sakein.

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

* **Why It Exists (Yeh kyun exist karta hai)**: Code ko users ke paas deploy karne se pehle compile-time par data mismatches, null values, aur contract breaking ko catch karta hai.
* **Real-World Analogy (Real-world Udaharan)**: **Construction Blueprints**. Concrete daalne se pehle blueprint specifications ko check karne se aap is baat se bach jaate hain ki baad me pata chale ki support pillars misaligned hain.

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
> **Interface vs Type (Interface vs Type)**: Public API structures aur classes ko declare karne ke liye `interface` ka use karein (declaration merging aur OOP extensibility ke karan). Complex unions, tuples, ya utility types ke liye `type` ka use karein.

---

## 04. Angular Architecture
🔗 **Full Lesson:** [04_Angular_Architecture.md](./04_Angular_Architecture.md)

* **Why It Exists (Yeh kyun exist karta hai)**: Boilerplate code ko kam karne aur tree-shaking performance ko behtar banane ke liye modular code bundling (`NgModule`) ko standalone component structures se replace karta hai.
* **Real-World Analogy (Real-world Udaharan)**: Ek **Self-Sufficient Smart Village**. Ek central electricity station jo utility configurations distribute karta hai (`NgModule`), uski jagah har ghar ke paas apne solar panels aur battery backup systems hain (Standalone components declaring imports).

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

* **Why It Exists (Yeh kyun exist karta hai)**: Presentation markup (HTML) aur UI logic (TS class) ko reusable, self-contained view modules me unify karta hai.
* **Real-World Analogy (Real-world Udaharan)**: **Vehicle Instrument Panel**. Engine controller (TS class) speed displays (Property Binding) ko update karta hai aur driver dial adjustment events (Event Binding) ko synchronously register karta hai.

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

* **Why It Exists (Yeh kyun exist karta hai)**: Component controllers ko formatting logic se pollute kiye bina HTML templates me dynamic variables ko format karta hai.
* **Real-World Analogy (Real-world Udaharan)**: **Water Filtration Nozzles**. Raw water pipe me enter karta hai; different nozzles output me mist, stream, ya spray options dete hain bina source water supply ko change kiye.

### Pure vs Impure Pipes:
* **Pure Pipe (Default)**: Sirf tabhi execute hota hai jab reference checks change hote hain (highly performant, cached calculations ka use karta hai).
* **Impure Pipe**: Har change detection cycle par execute hota hai (agar heavy tasks perform kar rahe hain toh performance issues create kar sakta hai).

### Key Pipes Syntax:
```html
<p>{{ price | currency:'EUR' }}</p>                       <!-- Built-in currency pipe -->
<p>{{ today | date:'yyyy-MM-dd' }}</p>                    <!-- Date pipe -->
<p>{{ userData$ | async }}</p>                            <!-- Async Pipe (Auto-unsubscribe) -->
```

---

## 07. Directives
🔗 **Full Lesson:** [07_Directives.md](./07_Directives.md)

* **Why It Exists (Yeh kyun exist karta hai)**: Elements me directly custom interactive behaviors (Attribute) attach karta hai ya conditionally DOM layout (Structural) ko restructure karta hai.
* **Real-World Analogy (Real-world Udaharan)**: **Wearable Sensor Badges**. Worker par ek badge pin karne se notifications trigger hoti hain jab wo unauthorized zones me enter karte hain, bina worker ke features ko modify kiye.

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

* **Why It Exists (Yeh kyun exist karta hai)**: Developers ko key runtime moments (initialization, change updates, aur destruction) se hook karta hai taaki async calls aur cleanup tasks execute kiye ja sakein.
* **Real-World Analogy (Real-world Udaharan)**: **Theatrical Play Stages**. Lighting set up karna (ngOnInit), actors ke bolne par scripts adjust karna (ngOnChanges), positions check karna (ngAfterViewInit), aur show ke end me set ko strike karna (ngOnDestroy).

### Lifecycle Order:
1. `Constructor`: Class instantiate hoti hai (yahan kabhi API calls nahi rakhni chahiye).
2. `ngOnChanges`: Tab trigger hota hai jab `@Input` variables ke references change hote hain.
3. `ngOnInit`: Component initialization (yahan data fetch karein).
4. `ngDoCheck`: Custom check handler.
5. `ngAfterViewInit`: HTML child template DOM queries fully initialized ho chuki hain.
6. `ngOnDestroy`: Cleanup phase (streams se unsubscribe karein, timers ko destroy karein).

---

## 09. Component Communication
🔗 **Full Lesson:** [09_Component_Communication.md](./09_Component_Communication.md)

* **Why It Exists (Yeh kyun exist karta hai)**: Nested parent-child component boundaries ke beech data sharing, UI events, aur structural templating ko coordinate karta hai.
* **Real-World Analogy (Real-world Udaharan)**: **Office Walkie-Talkies**. Parent managers tasks ko niche broadcast karte hain (Inputs), aur worker components alert pings ke zariye report back karte hain (Outputs).

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

* **Why It Exists (Yeh kyun exist karta hai)**: Status reads ko track karne ke liye fine-grained reactivity introduce karta hai. Yeh sirf change se affected DOM elements ko update karta hai, jisse Zone.js dirty-checking overhead bypass ho jata hai.
* **Real-World Analogy (Real-world Udaharan)**: **Spreadsheet Cells**. Cell `A1` me value change karne se formula ke zariye cell `C1` immediately update ho jata hai bina spreadsheet ke baaki cells ko check kiye.

### Signals Syntax:
```typescript
const count = signal(0);                                  // Writable Signal
const doubleCount = computed(() => count() * 2);          // Computed Signal (Cached)
const effectRef = effect(() => console.log(`Count changed to: ${count()}`)); // Effect (runs on changes)

count.set(5);                                             // Direct value write
count.update(val => val + 1);                             // Calculate new state
```

---

## 11. Dependency Injection
🔗 **Full Lesson:** [11_Dependency_Injection.md](./11_Dependency_Injection.md)

* **Why It Exists (Yeh kyun exist karta hai)**: Component logic ko instance creations se decouple karta hai, jisse test mocking enable hoti hai aur service instances centralize hote hain.
* **Real-World Analogy (Real-world Udaharan)**: Ek **Central Supply Closet**. Har builder dwara apni drill manufacture karne (naye services instantiate karne) ke bajaye, wo supplier (DI Injector) se ek drill provide karne ko kehte hain.

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

* **Why It Exists (Yeh kyun exist karta hai)**: Computational state, data mapping, aur API networking logic ko separate karke UI components ko bloat hone se rokta hai.
* **Real-World Analogy (Real-world Udaharan)**: **Restaurant Waiter & Kitchen**. Waiter (Component) sirf orders leta hai aur plates serve karta hai; kitchen (Service) ingredients source karna, cooking karna, aur plating manage karta hai.

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

* **Why It Exists (Yeh kyun exist karta hai)**: Browser URL configurations ke basis par client code me page views ko dynamically switch karta hai, jisse full page reloads nahi hote.
* **Real-World Analogy (Real-world Udaharan)**: **Airport Terminals**. Central runway fixed rehta hai; boarding tickets ke dynamic route parameters ke basis par passengers ko alag gates (components) par route kiya jata hai.

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

* **Why It Exists (Yeh kyun exist karta hai)**: HTML templates me directive bindings ka use karke quick, declarative forms create karta hai.
* **Real-World Analogy (Real-world Udaharan)**: **Paper Questionnaires**. Sheet par directly inputs ko fill karein; iska formatting aur fields paper par hi predefined hote hain.

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

* **Why It Exists (Yeh kyun exist karta hai)**: Class files ke andar complex form fields ko build, validate, dynamically-track, aur test karne ke liye ek programmatic, type-safe API provide karta hai.
* **Real-World Analogy (Real-world Udaharan)**: **Programmatic Spreadsheets**. Code me cell-by-cell validation constraints create karna, input values check karna, aur real-time me rules calculate karna.

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

* **Why It Exists (Yeh kyun exist karta hai)**: Backend networking requests ko handle karta hai, JSON payloads ko automatically parse karta hai, aur headers/tokens ko globally handle karta hai.
* **Real-World Analogy (Real-world Udaharan)**: **Registered Shipping Clerk**. Letters ko building se bahar bhejne se pehle unpar custom delivery stamps (Auth headers) lagana aur signatures verification handle karna.

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

* **Why It Exists (Yeh kyun exist karta hai)**: Functional programming paradigm ka use karke complex asynchronous event streams, timeouts, aur API dependencies ko manage karta hai.
* **Real-World Analogy (Real-world Udaharan)**: **Assembly Conveyor Belt**. Box me pack karne se pehle belt par items ko divert, aggregate, aur transform karna (operators ka use karke).

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

* **Why It Exists (Yeh kyun exist karta hai)**: Enterprise layouts me single source of truth ko maintain karke state scattering ko rokta hai.
* **Real-World Analogy (Real-world Udaharan)**: **Company Ledger**. Database discrepancies ko rokne ke liye sirf accounts desk (Reducers) hi transaction slips (Actions) ke zariye accounts ko update kar sakti hai.

### Store Architecture:
* **Actions**: Event ko describe karte hain (e.g. `[Cart] Add Item`).
* **Reducers**: Actions ke basis par new state calculate karne wale pure functions.
* **Selectors**: State tree se specific fields ko fetch karne ke liye queries.
* **Effects**: Asynchronous side-effects (e.g. API data fetch karna).

---

## 19. Authentication and Authorization
🔗 **Full Lesson:** [19_Authentication_and_Authorization.md](./19_Authentication_and_Authorization.md)

* **Why It Exists (Yeh kyun exist karta hai)**: Tokens, expiry validation checks, aur role mappings ko manage karke client routes aur API requests ko secure karta hai.
* **Real-World Analogy (Real-world Udaharan)**: **Theme Park Passes**. Wristbands (Tokens) ride zones me entry grant karte hain; expired passes ticket booths (Refresh Tokens) par automatically renew ho jate hain.

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

* **Why It Exists (Yeh kyun exist karta hai)**: Ready-made material design components (Data Tables, Dialogs, Inputs) ka use karke application UIs ko standardize karta hai.
* **Real-World Analogy (Real-world Udaharan)**: **Modular Building Blocks**. Custom bricks ko bake karne ke bajaye, aap built-in accessibility wale modular panels ko assemble karte hain.

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

* **Why It Exists (Yeh kyun exist karta hai)**: Initial page load times ko reduce karta hai aur runtime execution speeds (change detection cycles) ko optimize karta hai.
* **Real-World Analogy (Real-world Udaharan)**: **Security Checkpoints**. Gharon par checks skip karna jab tak unki gate alarm trigger na ho (`OnPush` change detection strategy).

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

* **Why It Exists (Yeh kyun exist karta hai)**: Code quality ko ensure karta hai aur changes likhte ya libraries upgrade karte waqt regression bugs ko rokta hai.
* **Real-World Analogy (Real-world Udaharan)**: **Flight Simulator**. Actual passengers ko fly karne se pehle cockpit responses ko different conditions me test karna.

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

* **Why It Exists (Yeh kyun exist karta hai)**: Applications ko malicious script injections (XSS) aur request hijackings (CSRF) se defend karta hai.
* **Real-World Analogy (Real-world Udaharan)**: **Mailroom Sterilizer**. Delivery se pehle mail automatically sanitize hota hai. Bypass karne ke liye managers override checks lagana mandatory hai.

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

* **Why It Exists (Yeh kyun exist karta hai)**: Node.js servers par templates ko pre-render karta hai taaki crawler indices (SEO) support ho sakein aur initial render delays reduce hon.
* **Real-World Analogy (Real-world Udaharan)**: **Meal Prepping**. Central kitchen (SSR server) me food cook karke package karna, taaki clients ko use sirf heat karna pade (Hydration).

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

* **Why It Exists (Yeh kyun exist karta hai)**: Code bases ko feature domains me divide karta hai, jisse infrastructure, services, aur smart vs dumb UI boundaries decouple hote hain.
* **Real-World Analogy (Real-world Udaharan)**: **Military Command Structure**. Command towers maneuvers decide karte hain (Smart Components), jabki front-line squads commands execute karte hain (Dumb Components).

### Smart Component (Container) vs Dumb Component (Presentation):
* **Smart**: Services inject karta hai, state streams manage karta hai, network APIs coordinate karta hai.
* **Dumb**: Reusable UI blocks, `@Input` ke zariye data accept karte hain, `@Output` ke zariye user events emit karte hain.

---

## 26. Deployment and CI/CD
🔗 **Full Lesson:** [26_Deployment_and_CI_CD.md](./26_Deployment_and_CI_CD.md)

* **Why It Exists (Yeh kyun exist karta hai)**: Build pipelines ko automate karta hai, stylesheets format karta hai, test suites run karta hai, aur server environments me compiled files ko push karta hai.
* **Real-World Analogy (Real-world Udaharan)**: **Manufacturing Shipping Center**. Quality check, pack boxes, stamp addresses, aur shipping containers ko automatically load karna.

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

* **Why It Exists (Yeh kyun exist karta hai)**: Lazy-loaded routes, state stores, secure authentication, API interceptors, aur checkout paths ka ek unified project me practical integration.
* **Real-World Analogy (Real-world Udaharan)**: **Online Mall**. Display shelves (catalog feature), user accounts (auth feature), cashiers (payment feature), aur shopping carts (state feature) ko integrate karta hai.

---

## 28. Beginner Interview Prep
🔗 **Full Lesson:** [28_Interview_Prep_Beginner.md](./28_Interview_Prep_Beginner.md)

* **Scope (Scope)**: Basic directive syntax, TypeScript bindings, aur setup workflows ke knowledge ko evaluate karta hai.
* **Example Question (Example Question)**: *What is the difference between `@Input` and `@Output`?*
  * **Answer**: `@Input` parent component se child component me data pass karta hai. `@Output` child se parent components me action events bubble karne ke liye `EventEmitter` ka use karta hai.

---

## 29. Interview Prep - Intermediate
🔗 **Full Lesson:** [29_Interview_Prep_Intermediate.md](./29_Interview_Prep_Intermediate.md)

* **Scope (Scope)**: Reactive form schemas, custom validation, pipes, directives, aur lifecycle hooks ke knowledge ko evaluate karta hai.
* **Example Question (Example Question)**: *What is the difference between Reactive Forms and Template-Driven Forms?*
  * **Answer**: Template-driven forms HTML template me declarative directives (jaise `ngModel`) ka use karte hain (simple, relies on two-way bindings). Reactive forms TypeScript class me programmatically declare hote hain (type-safe, scalable, testable, runs via RxJS streams).

---

## 30. Interview Prep - Advanced
🔗 **Full Lesson:** [30_Interview_Prep_Advanced.md](./30_Interview_Prep_Advanced.md)

* **Scope (Scope)**: Custom DI providers, performance, change detection, complex RxJS operators, aur token refresh interceptors ko evaluate karta hai.
* **Example Question (Example Question)**: *Explain how OnPush change detection improves performance.*
  * **Answer**: Default change detection poore component tree ko traverse karta hai. `OnPush` Angular ko component aur uske children ko check karne se skip karne ko kehta hai jab tak uski `@Input` property references update na hon, component event fire na ho, ya manually change detection trigger na kiya jaye.

---

## 31. Scenario and System Design
🔗 **Full Lesson:** [31_Interview_Prep_Scenario_and_System_Design.md](./31_Interview_Prep_Scenario_and_System_Design.md)

* **Scope (Scope)**: Enterprise systems architecture, monorepos, state management boundaries, caching interceptors, aur SSR hydration.
* **Example Question (Example Question)**: *How do you build a caching HTTP interceptor in Angular?*
  * **Answer**: Ek Map cache use karein. Interceptor outgoing `GET` requests ko intercept karta hai, check karta hai ki URL map cache me hai ya nahi, aur agar hai, toh cached `HttpResponse` observable return karta hai. Agar nahi hai, toh network call execute karta hai, map cache me response save karta hai, aur expiration timer set karta hai.

---
Previous : [00_index.md](./00_index.md) | Index : [00_index.md](./00_index.md) | Next : [01_Introduction_to_Angular.md](./01_Introduction_to_Angular.md)
