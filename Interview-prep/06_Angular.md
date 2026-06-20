# 🚀 Interview Preparation - Angular

> **Domain:** Web Development / Frontend  
> **Level:** Beginner to Expert  
> **Target Role:** Software Engineer / Senior Engineer / Lead

---

## 🟢 Beginner Level

### ❓ Q1. **What is Angular and how does it differ from AngularJS?**
<details>
<summary><b>👀 Show Answer</b></summary>

**Angular** (often referred to as Angular 2+) is a component-based, TypeScript-driven frontend framework developed by Google. It is a complete rewrite of the legacy **AngularJS** (Angular 1.x) framework.

| Feature | AngularJS (1.x) | Modern Angular (2+) |
| :--- | :--- | :--- |
| **Architecture** | MVC (Model-View-Controller) based | Component-based architecture |
| **Language** | Plain JavaScript | TypeScript (strongly typed) |
| **Mobile Support** | Not designed for mobile (poor performance) | Mobile-first design (runs natively on mobile) |
| **Data Binding** | Two-way binding via `$scope digest cycles` | Unidirectional data flow (OnPush / Signals) |
| **SEO Support** | Hard to implement | Built-in SSR (Server-Side Rendering) & Hydration |

> 💡 **Interviewer Focus:** Understanding the architecture shift from MVC controllers to independent components and TypeScript.

</details>
<hr/>

### ❓ Q2. **Explain the purpose of Standalone Components in modern Angular.**
<details>
<summary><b>👀 Show Answer</b></summary>

In legacy Angular, every component had to be registered in a parent `@NgModule` wrapper before it could be used. **Standalone Components** (introduced in Angular 14+) bypass modules by setting `standalone: true` in the `@Component` decorator, making the component independent.

#### 💬 Hinglish Explanation & Analogy:
* **Pehle (NgModule System):** Pehle Angular mein component akele run nahi ho sakta tha. Use ek wrapper box (`NgModule`) ke andar register karna padta tha. Agar aapko kisi page par ek simple text box ya button use karna hai, toh pehle use dynamic modules mein import/export karo. Isse bohot boilerplate code likhna padta tha.
* **Ab (Standalone System):** Component class direct metadata metadata setup configures block create kar sakta hai. `standalone: true` set karte hi component azaad ho jata hai. Ab us component ko use karne ke liye kisi module register ki zaroorat nahi hai. Uski apni jo dependencies hain (jaise direct buttons, text fields ya common templates directives), unhe direct component metadata metadata parameters `imports: [...]` ke andar mention kiya jata hai.
* **Bungalow vs Independent Flat Analogy:** 
  * *NgModule* ek bada joint-family bungalow hai, jahan agar kisi ko nayi machine (pipe/directive) lani hai toh poore ghar ke system registry/module file change setup rules se guzar kar declare karna padta tha.
  * *Standalone Component* ek independent modern flat ki tarah hai, jahan flat ka builder/owner direct apni machines and layout details (`imports`) flat ke andar hi install kar leta hai bina poor bungalow config check settings ke.
* **Performance optimization (Tree Shaking):** Agar koi module use nahi ho raha, toh build ke time bundler (esbuild/webpack) use remove kar deta hai (Tree Shaking), jisse initial loading code dynamic performance optimize ho jati hai.

```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonComponent } from './button.component';

@Component({
  selector: 'app-card',
  standalone: true, // Makes this component independent
  imports: [CommonModule, ButtonComponent], // Declare dependencies directly
  template: `
    <div class="card">
      <h3>Standalone Card</h3>
      <app-button label="Submit"></app-button>
    </div>
  `
})
export class CardComponent {}
```

> 💡 **Interviewer Focus:** How standalone components eliminate NgModules, simplify lazy loading, and optimize tree-shaking.


</details>
<hr/>

### ❓ Q3. **What is the difference between `@Component` and `@Directive`?**
<details>
<summary><b>👀 Show Answer</b></summary>

* **`@Component`** is a specialized directive that has an associated **HTML template** and styling definitions. It is the building block of Angular UI.
* **`@Directive`** does not have a template. It is used to attach styling, behavior, or structural logic to an existing DOM element.

#### 💬 Hinglish Explanation & Analogy:
* **Basic Antar (Difference):** 
  * `@Component` ek visual boundary/view control block hai jiske paas apna HTML view template aur unique styles configuration properties hoti hain. Angular application ka visual component trees isi se design hota hai.
  * `@Directive` ke paas **apna koi HTML template nahi hota**. Yeh directly standard DOM inputs/elements ke behaviors or custom CSS styling styles dynamically expand karne ke liye attach hoti hai.
* **Smart TV vs Remote/Firestick Analogy:**
  * **`@Component`** ek *Smart TV* screen hai, jiske paas display template window hai contents display karne ke liye.
  * **`@Directive`** ek *Remote controller* ya *Firestick adapter* hai jiske paas screen toh nahi hai par use TV (DOM host) ke sath plug karne par screen ka behavior or color values control kiya ja sakta hai.


```typescript
// Component: Has view template
@Component({
  selector: 'app-card',
  template: '<div class="card">Text</div>'
})
export class CardComponent {}

// Directive: No template, interacts with host element directly
@Directive({
  selector: '[appHighlight]'
})
export class HighlightDirective {
  constructor(private el: ElementRef) {
    this.el.nativeElement.style.backgroundColor = 'yellow';
  }
}
```

> 💡 **Interviewer Focus:** Components are directives with views. Directives modify existing views.

</details>
<hr/>

### ❓ Q4. **What is a Directive, and what are its three main types?**
<details>
<summary><b>👀 Show Answer</b></summary>

A **Directive** is a class decorated with `@Directive` that manipulates the appearance, behavior, or structure of DOM elements. 

#### The Three Types of Directives:
1. **Components:** Directives with templates (`@Component`).
2. **Attribute Directives:** Modify the style, layout, or behavior of an existing element (e.g., `ngStyle`, `ngClass`, or custom directives).
3. **Structural Directives:** Modify the structure of the DOM by adding, removing, or replacing elements (prefixed with `*` in template syntax, e.g., `*ngIf`, `*ngFor` or using `@if`, `@for` in modern Angular).

> 💡 **Interviewer Focus:** Categorization of directives and explaining the role of structural vs attribute directives.

</details>
<hr/>

### ❓ Q5. **Explain Property Binding vs Attribute Binding vs Interpolation.**
<details>
<summary><b>👀 Show Answer</b></summary>

* **Interpolation (`{{ value }}`):** Converts expressions to string structures and binds them directly into the element's text.
* **Property Binding (`[property]="value"`):** Binds values directly to DOM element properties (e.g. `[disabled]`, `[src]`), supporting complex types like booleans, arrays, or objects.
* **Attribute Binding (`[attr.name]="value"`):** Used specifically when the target property does not exist on the DOM object, but is required as an HTML attribute (e.g., `colspan`, `aria-label`).

```html
<!-- Interpolation -->
<p>Welcome, {{ username }}</p>

<!-- Property Binding -->
<button [disabled]="isPending">Submit</button>

<!-- Attribute Binding -->
<td [attr.colspan]="columnCount">Span Cell</td>
```

> 💡 **Interviewer Focus:** Recognizing that properties are DOM features, whereas attributes are HTML features.

</details>
<hr/>

### ❓ Q6. **What is the role of the Angular CLI?**
<details>
<summary><b>👀 Show Answer</b></summary>

The **Angular CLI** (Command Line Interface) is a tool used to initialize, develop, test, scaffold, build, and deploy Angular applications.

#### Common CLI Commands:
* `ng new <app-name>`: Initializes a workspace.
* `ng serve`: Runs a local dev server with hot reloading.
* `ng generate <type> <name>` (or `ng g <type> <name>`): Scaffolds components, services, pipes, directives, and guards with corresponding unit test files automatically.
* `ng build`: Compiles production-ready static assets.

> 💡 **Interviewer Focus:** Practical familiarity with modern CLI commands and automatic unit test generation.

</details>
<hr/>

### ❓ Q7. **What are lifecycle hooks? Name at least 5 common ones.**
<details>
<summary><b>👀 Show Answer</b></summary>

**Lifecycle hooks** are specific methods provided by Angular interfaces that execute at key moments during a component's lifecycle, from instantiation to destruction.

#### ⚙️ Common Lifecycle Hooks:
1. **`ngOnChanges`**: Fires when `@Input` properties update.
2. **`ngOnInit`**: Fires once after inputs are initialized (recommended for API/data fetching).
3. **`ngDoCheck`**: Runs custom change detection checks on every cycle.
4. **`ngAfterViewInit`**: Fires once after the component template view and child views are fully loaded into the DOM.
5. **`ngOnDestroy`**: Fires right before destruction (essential to clean up subscriptions and timers).

> 💡 **Interviewer Focus:** Hook execution order and where initialization vs cleanup should occur.

</details>
<hr/>

### ❓ Q8. **What is the purpose of the safe navigation operator (`?.`) in templates?**
<details>
<summary><b>👀 Show Answer</b></summary>

The **safe navigation operator (`?.`)** prevents Angular templates from throwing a `TypeError: Cannot read properties of null (reading '...')` error when evaluating paths where values might be `null` or `undefined`.

```html
<!-- Throws error if user is null -->
<p>{{ user.profile.name }}</p>

<!-- Safe: renders empty if user or profile is missing -->
<p>{{ user?.profile?.name }}</p>
```

> 💡 **Interviewer Focus:** Protecting templates from rendering crash bugs due to asynchronous loading.

</details>
<hr/>

### ❓ Q9. **What is the difference between `@ViewChild`, `@ViewChildren`, `@ContentChild`, and `@ContentChildren`?**
<details>
<summary><b>👀 Show Answer</b></summary>

* **`@ViewChild` / `@ViewChildren`**: Used to query and reference elements, directives, or child components that are declared directly in the component's **own HTML template**.
* **`@ContentChild` / `@ContentChildren`**: Used to query and reference elements or directives that are projected into the component via **content projection (`<ng-content>`)** from a parent template.

```typescript
@Component({
  selector: 'app-dashboard',
  template: `
    <app-chart #myChart></app-chart>
    <ng-content></ng-content>
  `
})
export class DashboardComponent {
  // Querying its own template component
  @ViewChild('myChart') chart!: ChartComponent;

  // Querying projected content component
  @ContentChild(ButtonComponent) projectedBtn!: ButtonComponent;
}
```

> 💡 **Interviewer Focus:** Querying local template elements vs projected content components.

</details>
<hr/>

### ❓ Q10. **What is a Template Reference Variable and how is it used?**
<details>
<summary><b>👀 Show Answer</b></summary>

A **Template Reference Variable** (declared using `#varName`) is a reference to a DOM element, directive, or child component within a template. It allows templates to share and query properties without involving component class logic.

```html
<!-- Accessing input value directly in the template -->
<input type="text" #userEmail placeholder="Email">
<button (click)="submit(userEmail.value)">Submit</button>
```

> 💡 **Interviewer Focus:** Simple template access rules, bypassing class logic properties.

</details>
<hr/>

### ❓ Q11. **Explain the difference between one-way and two-way data binding.**
*(No answer provided. Discuss the target syntax differences and performance implications of `[(ngModel)]`.)*
<hr/>

### ❓ Q12. **How does an Angular application bootstrap itself?**
*(No answer provided. Discuss the index.html file, main.ts file, and the bootstrapApplication API.)*
<hr/>

### ❓ Q13. **What is the purpose of the tsconfig.json file?**
*(No answer provided. Discuss how strict configurations prevent coding exceptions.)*
<hr/>

### ❓ Q14. **What is a single page application (SPA)?**
*(No answer provided. Discuss how DOM updates prevent browser document refreshes.)*
<hr/>

### ❓ Q15. **What is standard styling encapsulation in Angular?**
*(No answer provided. Discuss Emulated, ShadowDom, and None encapsulation modes.)*
<hr/>

### ❓ Q16. **What does the @Injectable decorator do?**
*(No answer provided. Discuss how it registers services to the dependency injection system.)*
<hr/>

### ❓ Q17. **What is the difference between constructor parameter initialization and standard property assignments?**
*(No answer provided. Discuss dependency injection mechanics.)*
<hr/>

### ❓ Q18. **What is npm and package.json?**
*(No answer provided. Discuss package locking dependencies.)*
<hr/>

### ❓ Q19. **What are the differences between HTML attributes and DOM properties?**
*(No answer provided. Discuss why property binding is preferred over attribute binding.)*
<hr/>

### ❓ Q20. **What are components?**
*(No answer provided. Discuss encapsulation boundaries.)*
<hr/>

### ❓ Q21. **How do you define input properties?**
*(No answer provided. Discuss `@Input` decorators and input signals.)*
<hr/>

### ❓ Q22. **What are template expression bindings?**
*(No answer provided. Discuss expression limits and side effects.)*
<hr/>

### ❓ Q23. **What is the standard workspace folder structure generated by the CLI?**
*(No answer provided. Discuss src, assets, and app layout directories.)*
<hr/>

### ❓ Q24. **How do you define inline styles vs external style sheets in components?**
*(No answer provided. Discuss component metadata configurations.)*
<hr/>

### ❓ Q25. **What are standalone dependencies?**
*(No answer provided. Discuss importing CommonModule or individual directives.)*
<hr/>

## 🟡 Intermediate Level

### ❓ Q26. **What is the purpose of `ngOnChanges` and when does it trigger?**
<details>
<summary><b>👀 Show Answer</b></summary>

**`ngOnChanges`** is a lifecycle hook that executes before `ngOnInit` and whenever Angular detects a change to any of the component's input properties (`@Input` bindings). 

#### ⚙️ How It Works:
* It receives a **`SimpleChanges`** object mapping the names of changed inputs to their current and previous values.
* **Important Constraint:** It only triggers if the **reference** of the input changes. Mutating an array element (`this.items.push(x)`) does not update the reference, so it will not trigger `ngOnChanges`.

```typescript
import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';

@Component({ ... })
export class ProfileComponent implements OnChanges {
  @Input() status = '';

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['status']) {
      const current = changes['status'].currentValue;
      const previous = changes['status'].previousValue;
      console.log(`Status changed from ${previous} to ${current}`);
    }
  }
}
```

> 💡 **Interviewer Focus:** Parameter references vs mutations, and tracking changes using the `SimpleChanges` object.

</details>
<hr/>

### ❓ Q27. **Explain standard structural directives vs new control flow syntax (`@if`, `@for`, `@switch`).**
<details>
<summary><b>👀 Show Answer</b></summary>

Prior to Angular 17, structural directives like `*ngIf` and `*ngFor` were imports from `CommonModule` that manipulated layouts. In Angular 17+, Angular introduced **Built-in Control Flow** (`@if`, `@for`, `@switch`), built directly into the template compiler.

| Feature | Legacy Directives (`*ngIf`, `*ngFor`) | Modern Control Flow (`@if`, `@for`) |
| :--- | :--- | :--- |
| **Imports** | Must import `CommonModule` or individual directives | Built-in, no imports required |
| **Syntax** | HTML attributes: `*ngIf="cond"` | Block syntax: `@if (cond) { ... }` |
| **Performance** | Higher parsing overhead | Up to 90% faster template rendering |
| **Track Parameter** | Optional `trackBy` function configurations | **Mandatory** `@for (item of items; track item.id)` parameter |

```html
<!-- Legacy structural directive -->
<div *ngIf="isLoggedIn; else guest">
  <p *ngFor="let user of users; trackBy: trackById">{{ user.name }}</p>
</div>
<ng-template #guest><p>Guest View</p></ng-template>

<!-- Modern Built-in Control Flow -->
@if (isLoggedIn) {
  @for (user of users; track user.id) {
    <p>{{ user.name }}</p>
  }
} @else {
  <p>Guest View</p>
}
```

> 💡 **Interviewer Focus:** Performance advantages, syntax changes, and why `track` is mandatory in modern `@for` loops.

</details>
<hr/>

### ❓ Q28. **What is Component Communication (Parent to Child, Child to Parent, Unrelated)?**
<details>
<summary><b>👀 Show Answer</b></summary>

Components can communicate in three ways:
1. **Parent to Child:** The parent passes data to the child component using property binding on the child's input properties (`@Input()` decorators or signal inputs).
2. **Child to Parent:** The child component raises events using an `@Output()` property binding configured as an `EventEmitter`. The parent listens to this event.
3. **Unrelated Components:** Communication is managed using shared services. Services use RxJS streams (like `BehaviorSubject`) or Angular `Signals` to broadcast state changes application-wide.

```typescript
// Child Component
@Component({
  selector: 'app-child',
  template: `<button (click)="notifyParent()">Notify</button>`
})
export class ChildComponent {
  @Input() data = '';
  @Output() trigger = new EventEmitter<string>();

  notifyParent() {
    this.trigger.emit('Action completed');
  }
}
```

> 💡 **Interviewer Focus:** Input/Output pipelines, EventEmitter logic, and when to delegate to a shared service wrapper.

</details>
<hr/>

### ❓ Q29. **What is a Pipe, and what is the difference between a Pure and an Impure Pipe?**
<details>
<summary><b>👀 Show Answer</b></summary>

A **Pipe** is a class decorated with `@Pipe` that transforms raw data into formatted values directly inside HTML templates.

#### Differences:
* **Pure Pipe (Default):** Runs only when its input reference changes (e.g. string/number change or array reference change). Results are cached, making pure pipes highly performant.
* **Impure Pipe:** Runs on every change detection cycle, regardless of whether inputs have changed. This allows it to detect mutations inside arrays (like `items.push()`), but can cause serious performance issues.

```typescript
// Pure Pipe: Only runs if reference changes
@Pipe({
  name: 'pureLength',
  pure: true,
  standalone: true
})
export class LengthPipe implements PipeTransform {
  transform(value: string): number {
    return value.length;
  }
}
```

> 💡 **Interviewer Focus:** Input reference caching, change detection cycles, and the performance impact of impure pipes.

</details>
<hr/>

### ❓ Q30. **Explain the `Async` pipe and why it is recommended.**
<details>
<summary><b>👀 Show Answer</b></summary>

The **`AsyncPipe`** is a built-in pipe that handles async data directly inside templates. It takes an Observable or a Promise, subscribes to it, yields the values, and automatically unsubscribes when the component is destroyed.

#### ⚙️ Why it is recommended:
1. **Prevents Memory Leaks:** Removes the need to write manual cleanups in `ngOnDestroy`.
2. **Keeps Code Declarative:** Eliminates class-level subscriptions, keeping components thin.
3. **Supports OnPush:** Automatically tells the change detector to check the component when new values emit.

```html
<!-- Automatically subscribes and handles cleanup -->
<div *ngIf="user$ | async as user">
  <p>{{ user.name }}</p>
</div>
```

> 💡 **Interviewer Focus:** Automatic subscription management, prevention of memory leaks, and seamless integration with `OnPush` change detection.

</details>
<hr/>

### ❓ Q31. **What is Dependency Injection (DI) and what is hierarchical injection?**
<details>
<summary><b>👀 Show Answer</b></summary>

**Dependency Injection (DI)** is a design pattern in which a class requests dependencies from an external system rather than creating them itself.

**Hierarchical Injection** refers to Angular's tree of injectors. If a component requests a dependency, Angular traverses the component injector tree upwards until it finds a provider:
1. **ElementInjector:** Providers registered in the component's `providers: [...]` or `viewProviders: [...]` arrays.
2. **EnvironmentInjector:** Providers registered in `bootstrapApplication()` config or `@Injectable({ providedIn: 'root' })`.
3. **ModuleInjector:** Legacy providers configured in `NgModule` arrays.

If registered at the component level, each component instance gets its own instance of the service. If registered as `root`, it is a global singleton.

> 💡 **Interviewer Focus:** Traversal rules from local Element Injector to the global Environment Injector.

</details>
<hr/>

### ❓ Q32. **What is `providedIn: 'root'` and how does it enable tree shaking?**
<details>
<summary><b>👀 Show Answer</b></summary>

Declaring `@Injectable({ providedIn: 'root' })` registers the service as a global singleton. 

#### Tree-Shaking Mechanism:
If a service is registered in a module's `providers: [...]` array, it will be included in the production bundle even if no component ever uses it. 

Using `providedIn: 'root'` enables **tree-shaking**: if the service is not imported anywhere in the application, the compiler excludes it from the final production JavaScript build, optimizing bundle size.

> 💡 **Interviewer Focus:** Difference between module registration and tree-shakable root injectables.

</details>
<hr/>

### ❓ Q33. **How do you implement a Custom Pipe?**
<details>
<summary><b>👀 Show Answer</b></summary>

To implement a custom pipe, create a class decorated with `@Pipe`, specify its name, and implement the **`PipeTransform`** interface's `transform` method.

```typescript
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'appTruncate',
  standalone: true
})
export class TruncatePipe implements PipeTransform {
  transform(value: string, limit: number = 10, suffix: string = '...'): string {
    if (!value) return '';
    return value.length > limit ? value.substring(0, limit) + suffix : value;
  }
}
```
**Usage in HTML:**
```html
<p>{{ longText | appTruncate:20:'...' }}</p>
```

> 💡 **Interviewer Focus:** Implementing `PipeTransform`, defining argument overrides, and importing it into standalone components.

</details>
<hr/>

### ❓ Q34. **How does `HttpClient` handle error propagation using RxJS catchError?**
<details>
<summary><b>👀 Show Answer</b></summary>

The `HttpClient` returns RxJS observables. Errors are intercepted in the observable stream using the **`catchError`** operator. This catches HTTP errors (like 401 or 500 status codes) and allows you to return a fallback value or propagate a formatted error message using `throwError`.

```typescript
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';

inject(HttpClient).get<User[]>('/api/users').pipe(
  catchError((error: HttpErrorResponse) => {
    let errMsg = 'An unknown error occurred';
    if (error.status === 404) errMsg = 'Resource not found';
    return throwError(() => new Error(errMsg));
  })
);
```

> 💡 **Interviewer Focus:** catchError usage, parsing `HttpErrorResponse`, and propagating errors using `throwError`.

</details>
<hr/>

### ❓ Q35. **What is the difference between element and host bindings?**
*(No answer provided. Discuss HostBinding and HostListener vs standard DOM modifications.)*
<hr/>

### ❓ Q36. **Explain what routing guards do.**
*(No answer provided. Discuss intercepting routes during navigation flows.)*
<hr/>

### ❓ Q37. **How do you pass queries and query parameters?**
*(No answer provided. Discuss ActivatedRoute snapshot access.)*
<hr/>

### ❓ Q38. **What is the purpose of HTTP interceptors?**
*(No answer provided. Discuss appending request tokens globally.)*
<hr/>

### ❓ Q39. **How do you manage nested route setups?**
*(No answer provided. Discuss children route lists and nested router outlets.)*
<hr/>

### ❓ Q40. **What is the difference between a custom directive and standard component?**
*(No answer provided. Discuss style decoration options.)*
<hr/>

### ❓ Q41. **Explain the trackBy function for template lists.**
*(No answer provided. Discuss tracking item IDs to optimize DOM updates.)*
<hr/>

### ❓ Q42. **What is view encapsulation and what is its default mode?**
*(No answer provided. Discuss why Emulated encapsulation is standard.)*
<hr/>

### ❓ Q43. **How do you share state using simple services?**
*(No answer provided. Discuss BehaviorSubject state patterns.)*
<hr/>

### ❓ Q44. **What is the difference between a Subject and a BehaviorSubject?**
*(No answer provided. Discuss value caching and default initial states.)*
<hr/>

### ❓ Q45. **What are standalone components dependencies routing?**
*(No answer provided. Discuss configuring routes inside providers.)*
<hr/>

### ❓ Q46. **What is the difference between view providers and standard providers?**
*(No answer provided. Discuss child component access scopes.)*
<hr/>

### ❓ Q47. **How do you resolve dynamic resources using route resolvers?**
*(No answer provided. Discuss fetching data before page transitions finish.)*
<hr/>

### ❓ Q48. **What is the purpose of custom directives?**
*(No answer provided. Discuss styling and behavior additions.)*
<hr/>

### ❓ Q49. **How do you handle event bubbling inside HostListeners?**
*(No answer provided. Discuss event stopPropagation calls.)*
<hr/>

### ❓ Q50. **What is the difference between dynamic and static components?**
*(No answer provided. Discuss ViewContainerRef and dynamically loading components.)*
<hr/>

## 🔴 Advanced Level

### ❓ Q51. **What are Angular Signals and how do they work?**
<details>
<summary><b>👀 Show Answer</b></summary>

**Angular Signals** (introduced in Angular 16+) are reactive values that track their dependencies and notify the system when they change. They represent a shift away from Zone.js towards **fine-grained reactivity**.

#### ⚙️ The Three Core Concepts:
1. **Writable Signals (`signal`):** Hold values that can be updated directly using `.set()` or `.update()`.
2. **Computed Signals (`computed`):** Read-only signals that derive their values from other signals. They are **lazily evaluated** and cached.
3. **Effects (`effect`):** Functions that run side effects (like logging or saving to localStorage) whenever any signal they read changes.

```typescript
import { signal, computed, effect } from '@angular/core';

// Writable Signal
const price = signal(100);
const qty = signal(2);

// Derived Signal (caches evaluation)
const total = computed(() => price() * qty());

// Effect logs automatically when dependencies change
effect(() => {
  console.log(`Grand Total is: ${total()}`);
});

qty.set(3); // Log output: "Grand Total is: 300"
```

> 💡 **Interviewer Focus:** Fine-grained reactivity, lazy evaluation of computed signals, and how they reduce change detection overhead.

</details>
<hr/>

### ❓ Q52. **Compare Signals with RxJS BehaviorSubjects.**
<details>
<summary><b>👀 Show Answer</b></summary>

While both manage state updates reactively, they serve different purposes:

| Feature | Angular Signals | RxJS BehaviorSubjects |
| :--- | :--- | :--- |
| **API Type** | Synchronous value tracking | Asynchronous event streams |
| **Read Syntax** | Simple function call: `mySignal()` | Asynchronous subscription or `.getValue()` |
| **Subscriptions** | Automatic dependency tracking | Manual subscription management |
| **Use Case** | Local state and UI data-binding | Async operations (HTTP, WebSockets, event logic) |
| **Side Effects** | Managed via standard `effect()` | Managed via RxJS pipe operators |

> 💡 **Interviewer Focus:** Signals are synchronous and excel at template binding; RxJS is asynchronous and excels at complex event streams. They are complementary, not mutually exclusive.

</details>
<hr/>

### ❓ Q53. **What is `ChangeDetectionStrategy.OnPush` and how does it improve performance?**
<details>
<summary><b>👀 Show Answer</b></summary>

By default, Angular uses the `Default` change detection strategy, which checks the entire component tree from top to bottom whenever any asynchronous event occurs (like a click, timer, or HTTP response).

Setting `changeDetection: ChangeDetectionStrategy.OnPush` instructs Angular to skip checking the component and its children unless:
1. One of its input properties (`@Input`) receives a **new reference**.
2. An event handler inside the component template triggers.
3. A bound observable emits a new value (via `async` pipe).
4. Change detection is requested manually using `ChangeDetectorRef.markForCheck()`.

```typescript
@Component({
  selector: 'app-heavy-list',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `<ul><li *ngFor="let item of items">{{ item }}</li></ul>`
})
export class HeavyListComponent {
  @Input() items: string[] = [];
}
```

> 💡 **Interviewer Focus:** Skipping component subtree checks, input references, and the role of the `markForCheck()` method.

</details>
<hr/>

### ❓ Q54. **Explain `@defer` blocks (Deferred Loading) and their triggers.**
<details>
<summary><b>👀 Show Answer</b></summary>

Introduced in Angular 17, the **`@defer`** template block enables **lazy loading** of components, directives, and pipes at the template level, keeping initial page load bundle sizes small.

#### ⚙️ Key Triggers:
* `on idle` (Default): Loads content once the browser is idle.
* `on viewport`: Loads content once it enters the browser viewport.
* `on interaction`: Loads content when the user clicks or focuses on a placeholder.
* `on hover`: Loads content when the user hovers over a placeholder.
* `when <condition>`: Loads content when a custom boolean expression evaluates to true.

```html
<!-- Prerenders a placeholder, then loads the heavy chart component
     when the placeholder enters the viewport -->
@defer (on viewport) {
  <app-heavy-chart></app-heavy-chart>
} @placeholder {
  <div class="skeleton">Chart is loading...</div>
} @loading {
  <p>Downloading bundles...</p>
} @error {
  <p>Failed to load chart.</p>
}
```

> 💡 **Interviewer Focus:** Declarative lazy loading in templates, placeholder/loading states, and the various trigger behaviors.

</details>
<hr/>

### ❓ Q55. **What is the difference between Reactive Forms and Template-Driven Forms?**
<details>
<summary><b>👀 Show Answer</b></summary>

| Feature | Template-Driven Forms | Reactive Forms |
| :--- | :--- | :--- |
| **Configuration** | Configured in HTML templates via directives | Configured programmatically in TypeScript classes |
| **Data Flow** | Asynchronous two-way data sync | Synchronous, predictable data flow |
| **Validation** | HTML validation attributes (e.g. `required`) | Programmatic validation functions |
| **Testing** | Hard to unit-test (requires DOM rendering) | Easy to unit-test without compiling templates |
| **Scalability** | Best for simple input layouts | Best for complex schemas and dynamic inputs |

```typescript
// Reactive Forms Example
export class RegistrationComponent {
  profileForm = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.email]),
  });
}
```

> 💡 **Interviewer Focus:** Code co-location, testing capabilities, and state predictability.

</details>
<hr/>

### ❓ Q56. **How do you write a custom Validator in Reactive Forms?**
<details>
<summary><b>👀 Show Answer</b></summary>

A custom validator is a function that takes an Angular **`AbstractControl`** as its argument and returns:
* **`ValidationErrors`** (a key-value object containing validation error keys) if validation fails.
* **`null`** if validation succeeds.

```typescript
import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

// Validator factory function
export function forbiddenNameValidator(nameRe: RegExp): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const forbidden = nameRe.test(control.value);
    // Returns error map if input matches forbidden name, else null
    return forbidden ? { forbiddenName: { value: control.value } } : null;
  };
}

// Usage in FormControl configuration:
const nameControl = new FormControl('', [forbiddenNameValidator(/admin/i)]);
```

> 💡 **Interviewer Focus:** Validator function signatures, parsing AbstractControl, and return error objects.

</details>
<hr/>

### ❓ Q57. **What is `HttpClient` and why does it return cold Observables?**
<details>
<summary><b>👀 Show Answer</b></summary>

**`HttpClient`** is Angular's built-in service to perform HTTP requests. It uses RxJS Observables under the hood.

#### ❄️ Cold Observables:
`HttpClient` methods return cold observables because HTTP requests are transactional. The network request is **not executed** until a subscriber calls `.subscribe()`. 

This allows developers to chain operators (such as `retry`, `catchError`, or `map`) to configure the request before sending it over the network.

```typescript
// No network call made yet
const request$ = this.http.get('/api/users');

// Network call is sent now
request$.subscribe(data => console.log(data));
```

> 💡 **Interviewer Focus:** Transactional nature of HTTP calls, and the difference between cold and hot observables.

</details>
<hr/>

### ❓ Q58. **How do HTTP Interceptors work and how do you write a functional interceptor?**
<details>
<summary><b>👀 Show Answer</b></summary>

**HTTP Interceptors** intercept and modify incoming or outgoing HTTP requests globally (e.g. to inject authorization headers, handle logging, or catch network errors).

In modern Angular (15+), interceptors are written as lightweight functions instead of classes.

```typescript
import { HttpInterceptorFn, HttpRequest, HttpHandlerFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (
  req: HttpRequest<unknown>, 
  next: HttpHandlerFn
) => {
  const token = localStorage.getItem('auth_token');
  
  // Clone the request to inject headers (requests are immutable)
  const modifiedReq = token ? req.clone({
    headers: req.headers.set('Authorization', `Bearer ${token}`)
  }) : req;
  
  return next(modifiedReq);
};
```
**Registration in Config:**
```typescript
bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(withInterceptors([authInterceptor]))
  ]
});
```

> 💡 **Interviewer Focus:** Request immutability (must clone), functional interceptor patterns, and how to register them in bootstrap configs.

</details>
<hr/>

### ❓ Q59. **What is the purpose of the `track` parameter inside the new `@for` template loop?**
<details>
<summary><b>👀 Show Answer</b></summary>

The **`track`** parameter inside the built-in `@for` loop determines how Angular identifies unique items in a list.

#### ⚙️ Why it matters:
When items in an array change, Angular uses the `track` key (usually an `id` or unique property) to identify which items have moved, been added, or been removed. 

Without `track`, Angular would have to destroy and recreate all DOM elements in the list on every change detection cycle, degrading performance. 

Unlike the legacy `trackBy` function, the new `@for` syntax requires `track` by default:

```html
<!-- Mandatory tracking key -->
@for (product of products; track product.id) {
  <li>{{ product.name }}</li>
}
```

> 💡 **Interviewer Focus:** DOM element reuse, performance gains over destroying elements, and modern syntax requirements.

</details>
<hr/>

### ❓ Q60. **How do you configure dynamic validation updates in Reactive Forms?**
*(No answer provided. Discuss updateValueAndValidity API calls.)*
<hr/>

### ❓ Q61. **Explain the difference between throttleTime and debounceTime.**
*(No answer provided. Discuss RxJS event filtering.)*
<hr/>

### ❓ Q62. **What are Route Guards resolvers and how do they differ from guards?**
*(No answer provided. Discuss data pre-loading vs navigation blockers.)*
<hr/>

### ❓ Q63. **How do you configure micro-frontend federations?**
*(No answer provided. Discuss loading external modules on demand.)*
<hr/>

### ❓ Q64. **Explain what the NgRx Effects pattern handles.**
*(No answer provided. Discuss handling asynchronous side-effects in NgRx stores.)*
<hr/>

### ❓ Q65. **How do you implement optimistic UI updates using state management?**
*(No answer provided. Discuss updating local state immediately while sending requests to backend.)*
<hr/>

### ❓ Q66. **What is structural directives context?**
*(No answer provided. Discuss TemplateRef and ViewContainerRef contexts.)*
<hr/>

### ❓ Q67. **How do you configure cross-origin resource sharing (CORS) locally?**
*(No answer provided. Discuss proxy.conf.json configuration setups.)*
<hr/>

### ❓ Q68. **What is the difference between dynamic imports and standard imports?**
*(No answer provided. Discuss lazy loading code bundles.)*
<hr/>

### ❓ Q69. **Explain change detection tree checks optimizations.**
*(No answer provided. Discuss NgZone bypass runOutsideAngular calls.)*
<hr/>

### ❓ Q70. **What is compile-time lazy loading?**
*(No answer provided. Discuss code-splitting configurations.)*
<hr/>

### ❓ Q71. **How do you configure custom route strategies?**
*(No answer provided. Discuss RouteReuseStrategy overrides.)*
<hr/>

### ❓ Q72. **What is the difference between valueChanges and statusChanges?**
*(No answer provided. Discuss forms status streams.)*
<hr/>

### ❓ Q73. **How do you mock HTTP services in unit tests?**
*(No answer provided. Discuss HttpTestingController assertions.)*
<hr/>

### ❓ Q74. **What is tree-shaking compilation?**
*(No answer provided. Discuss static analysis during production builds.)*
<hr/>

### ❓ Q75. **How do you configure content projection slots?**
*(No answer provided. Discuss select attributes on ng-content elements.)*
<hr/>

## 🟣 Expert Level

### ❓ Q76. **Explain RxJS flattening operators (`switchMap`, `mergeMap`, `concatMap`, `exhaustMap`) with real-world scenarios.**
<details>
<summary><b>👀 Show Answer</b></summary>

Flattening operators map an outer observable stream to an inner observable stream, handling the inner subscriptions automatically. Choosing the right one is crucial for performance and consistency:

1. **`switchMap` (Cancel/Switch):** Cancels the active inner observable subscription when a new emission arrives.
   * *Real-world Scenario:* Search autocomplete. As the user types, older search requests are aborted immediately, and only the latest API query executes.
2. **`mergeMap` (Concurrence):** Subscribes to all inner observables concurrently as they arrive.
   * *Real-world Scenario:* File uploads. If a user selects 5 files to upload at once, they run in parallel.
3. **`concatMap` (Queue/Transaction):** Queues inner observables, executing them sequentially in order.
   * *Real-world Scenario:* Chat messaging logs. Keeps messages in order, ensuring message 1 renders before message 2 starts.
4. **`exhaustMap` (Lock/Ignore):** Ignores new emissions while the current inner observable is running.
   * *Real-world Scenario:* Submit button. If a user double-clicks "Submit Order", the second click is ignored until the first API call finishes, preventing duplicate orders.

> 💡 **Interviewer Focus:** Distinct behavior patterns of each operator, queueing vs cancellation, and applying them to real-world scenarios.

</details>
<hr/>

### ❓ Q77. **What is SSR (Server-Side Rendering) in Angular, and how does non-destructive hydration work?**
<details>
<summary><b>👀 Show Answer</b></summary>

**Server-Side Rendering (SSR)** pre-renders static HTML pages on a Node.js server before sending them to the client, improving SEO indexability and first-paint times.

#### ⚙️ Non-Destructive Hydration:
In legacy SSR (like Angular Universal), the client would discard the server-rendered HTML and rebuild the entire DOM tree from scratch, causing noticeable screen flickering.

In modern Angular (16+), **non-destructive hydration** preserves the server-rendered HTML and simply attaches event listeners and state directly to the existing elements, making them interactive without recalculating layout structures or recreating DOM nodes.

> 💡 **Interviewer Focus:** Non-destructive vs destructive hydration, edge rendering, and avoiding flickering.

</details>
<hr/>

### ❓ Q78. **What are Route Guards? Explain `CanActivate` vs `CanMatch`.**
<details>
<summary><b>👀 Show Answer</b></summary>

Route guards secure routes in Angular by determining whether a route transition can complete.

* **`CanActivate`**: Determines if a route can be activated. However, the route component's code bundle is **already downloaded** before the guard runs. If block triggers, bundle download overhead is wasted.
* **`CanMatch`**: Determines if a route configuration matches a path. It executes **before** route bundles are downloaded. If block triggers, the bundle is never downloaded, and Angular falls back to alternative path mappings.

```typescript
// CanMatchFn prevents chunk downloads for unauthorized users
export const adminGuard: CanMatchFn = (route, segments) => {
  const auth = inject(AuthService);
  return auth.isAdmin(); // Returns boolean observable
};
```

> 💡 **Interviewer Focus:** Performance differences, bundle downloading scopes, and when to use `CanMatch` over `CanActivate`.

</details>
<hr/>

### ❓ Q79. **How do you implement state management using NgRx Signal Store?**
<details>
<summary><b>👀 Show Answer</b></summary>

The **NgRx Signal Store** is a lightweight, functional state management library built on top of Angular's Signals API. It replaces classic, boilerplate-heavy NgRx (reducers, actions, effects) with a clean, composition-based structure.

#### ⚙️ Key Concepts:
1. **`signalStore`**: Creates a state store with signals.
2. **`withState`**: Defines the initial state object.
3. **`withComputed`**: Defines derived read-only state properties.
4. **`withMethods`**: Defines methods to update the state.

```typescript
import { signalStore, withState, withComputed, withMethods, patchState } from '@ngrx/signals';

export interface TodoState {
  todos: string[];
}

export const TodoStore = signalStore(
  { providedIn: 'root' },
  withState<TodoState>({ todos: [] }),
  withComputed(({ todos }) => ({
    count: computed(() => todos().length),
  })),
  withMethods((store) => ({
    addTodo(todo: string) {
      patchState(store, { todos: [...store.todos(), todo] });
    },
  }))
);
```

> 💡 **Interviewer Focus:** State mutation using `patchState`, defining actions inside `withMethods`, and the simplified syntax compared to classic NgRx.

</details>
<hr/>

### ❓ Q80. **What are zone.js and zoneless Angular?**
<details>
<summary><b>👀 Show Answer</b></summary>

#### `Zone.js` (Legacy Change Detection):
Angular has historically relied on `Zone.js` to intercept asynchronous tasks (like clicks, timeouts, and HTTP requests). Whenever an async operation finishes, `Zone.js` triggers change detection across the entire component tree to find what changed. This is expensive and hard to optimize.

#### Zoneless Angular (Modern):
With the introduction of **Signals** (Angular 18+), Angular can now track precisely *which* templates depend on *which* values. 

This enables **Zoneless change detection**, which removes `Zone.js` from the application completely. When a signal changes, Angular updates only the specific DOM nodes linked to that signal, improving rendering performance and reducing initial bundle sizes.

> 💡 **Interviewer Focus:** How Zone.js works (monkey-patching browser APIs), change detection overhead, and how Signals enable zoneless architectures.

</details>
<hr/>

### ❓ Q81. **How do you secure an Angular app against XSS?**
<details>
<summary><b>👀 Show Answer</b></summary>

Angular is designed to protect applications from Cross-Site Scripting (XSS) attacks.

#### 🛡️ Built-in Protections:
1. **Automatic Sanitization:** Angular sanitizes all user values before binding them in templates, stripping out unsafe HTML tags (like `<script>` or `<iframe>`) and inline styles.
2. **Contextual Evaluation:** Angular evaluates values based on their destination context (HTML, attribute, style, or URL).
3. **DomSanitizer:** If you need to bind dynamic trust resources (like safe HTML or iframe sources), you must bypass default sanitization using `DomSanitizer` methods (such as `bypassSecurityTrustHtml`). Use these with caution, and only on pre-sanitized values.

```typescript
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

export class SafeHtmlComponent {
  trustedHtml: SafeHtml;

  constructor(private sanitizer: DomSanitizer) {
    // Manually trust the value to bypass security
    this.trustedHtml = this.sanitizer.bypassSecurityTrustHtml(
      '<div onclick="maliciousCode()">Safe markup wrapper</div>'
    );
  }
}
```

> 💡 **Interviewer Focus:** Automatic sanitization, contextual validation, and the security risks associated with `DomSanitizer`.

</details>
<hr/>

### ❓ Q82. **What is Module Federation and how is it used in micro-frontends?**
<details>
<summary><b>👀 Show Answer</b></summary>

**Module Federation** is a Webpack/Esbuild compiler capability that allows an application to dynamically load compiled code modules from a completely separate build project at runtime.

#### ⚙️ How it works in Micro-Frontends:
1. **Shell Application:** Acts as the host container. It configures paths and routes to look up components from remote applications at runtime.
2. **Remote Applications:** Compile and expose feature modules (such as billing, catalog) independently.
3. **Runtime Sharing:** At runtime, the Shell loads the remote bundles on-demand, sharing common dependencies (like Angular core or shared CSS libraries) to prevent downloading duplicate packages.

This allows multiple development teams to deploy feature updates independently without needing to compile or deploy the main container shell application.

> 💡 **Interviewer Focus:** Runtime loading vs compile-time bundling, sharing core dependencies, and shell vs remote setups.

</details>
<hr/>

### ❓ Q83. **How do you optimize large-scale Angular builds using Nx monorepos?**
<details>
<summary><b>👀 Show Answer</b></summary>

**Nx** is a build system that optimizes monorepos by using caching and dependency graph analysis:

1. **Affected Builds:** Instead of building and testing all projects in the monorepo, Nx analyzes changes (`nx affected:build`) and only rebuilds projects that were actually modified.
2. **Computational Caching:** Nx hashes build tasks and caches their outputs locally and in the cloud. If you run a task (like unit testing) that has already been executed on a team member's machine or in CI, Nx retrieves the cached results instantly instead of running the task again.
3. **Strict Boundary Rules:** Nx lets you define dependency rules to prevent feature domains from importing files from unrelated features, keeping the architecture decoupled.

> 💡 **Interviewer Focus:** Affected builds, build caching, and enforcing dependency boundary rules.

</details>
<hr/>

### ❓ Q84. **Explain how to prevent ExpressionChangedAfterItHasBeenCheckedError.**
*(No answer provided. Discuss when views update after check validations.)*
<hr/>

### ❓ Q85. **What is dynamic route compilation?**
*(No answer provided. Discuss loading modules using path configurations.)*
<hr/>

### ❓ Q86. **How do you configure custom decorators in Angular?**
*(No answer provided. Discuss building TypeScript method/class decorators.)*
<hr/>

### ❓ Q87. **What is the difference between Webpack and Esbuild compilers in Angular builds?**
*(No answer provided. Discuss speed improvements and compilation processes.)*
<hr/>

### ❓ Q88. **Explain how to debug memory leaks in Angular components.**
*(No answer provided. Discuss Chrome DevTools heap snapshot checks.)*
<hr/>

### ❓ Q89. **What are route reuse strategies?**
*(No answer provided. Discuss caching routed views to prevent destroy cycles.)*
<hr/>

### ❓ Q90. **How do you implement offline synchronization patterns?**
*(No answer provided. Discuss IndexedDB configurations and Service Workers.)*
<hr/>

### ❓ Q91. **What is the purpose of NgZone and how do you bypass it?**
*(No answer provided. Discuss runOutsideAngular calls for high-frequency events.)*
<hr/>

### ❓ Q92. **How do you configure custom control value accessors (NG_VALUE_ACCESSOR)?**
*(No answer provided. Discuss binding custom UI inputs to Reactive Forms.)*
<hr/>

### ❓ Q93. **What is the difference between static and dynamic hydration?**
*(No answer provided. Discuss progressive hydration methods.)*
<hr/>

### ❓ Q94. **Explain how content security policies (CSP) are configured.**
*(No answer provided. Discuss nonces for inline styles and scripts.)*
<hr/>

### ❓ Q95. **How do you profile change detection cycles using Angular DevTools?**
*(No answer provided. Discuss flame graphs and checking execution times.)*
<hr/>

### ❓ Q96. **What is the compile process under Ivy?**
*(No answer provided. Discuss incremental template compiling.)*
<hr/>

### ❓ Q97. **Explain how to configure custom template outlets.**
*(No answer provided. Discuss NgTemplateOutlet contexts.)*
<hr/>

### ❓ Q98. **How do you implement tree-shakability for custom components?**
*(No answer provided. Discuss standalone exports.)*
<hr/>

### ❓ Q99. **What are web workers and how do you leverage them in Angular?**
*(No answer provided. Discuss offloading heavy computations from the UI thread.)*
<hr/>

### ❓ Q100. **Explain dynamic configuration loading before application boot.**
*(No answer provided. Discuss APP_INITIALIZER tokens.)*
<hr/>

---

### 🧭 Navigation

| ⬅️ Previous | 🏠 Index | ➡️ Next |
| :--- | :---: | ---: |
| [⬅️ React Native](./05_ReactNative.md) | [Home](./00_Index.md) | [➡️ Khelo Tech Prep](./khelo_tech.md) |
