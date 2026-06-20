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
* **Ab (Standalone System):** Component class direct metadata setup configures block create kar sakta hai. `standalone: true` set karte hi component azaad ho jata hai. Ab us component ko use karne ke liye kisi module register ki zaroorat nahi hai. Uski apni jo dependencies hain (jaise direct buttons, text fields ya common templates directives), unhe direct component metadata parameters `imports: [...]` ke andar mention kiya jata hai.
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
  * `@Directive` ke paas **apna koi HTML template nahi hota**. Element level custom behavior or attributes change dynamic behaviors support rules provide karne ke liye directives utilize hoti hain.
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

**Lifecycle hooks** are specific methods provided by Angular interfaces that execute at key moments during a component's lifecycle—from its creation to its destruction. They allow us to intercept these phases and run custom logic (like fetching API data, setting up event listeners, or cleaning up memory).

```
🔄 Component Lifecycle Hook Execution Order:
Constructor ──> ngOnChanges ──> ngOnInit ──> ngDoCheck
                 ──> ngAfterContentInit ──> ngAfterContentChecked
                 ──> ngAfterViewInit ──> ngAfterViewChecked ──> ngOnDestroy
```

#### 💬 Hinglish Explanations & Analogies of Key Hooks:

##### 1. **`constructor()`** (Class Instantiation)
* **What it does:** Yeh ES6 class ka standard constructor hai. Is stage par Angular dependency injection (DI) ko resolve karta hai, par inputs (`@Input`) ya DOM template structure ready nahi hota.
* **Hinglish Analogy:** Ghar ki registry hona. Ghar ban gaya hai par furniture (data/inputs) abhi tak nahi aaya hai.

##### 2. **`ngOnChanges()`** (Input Binding updates)
* **What it does:** Har baar jab component ka `@Input` value badalta hai, tab yeh method trigger hota hai. Isko ek `SimpleChanges` object milta hai jisme current aur previous values hoti hain.
* **Hinglish Analogy:** Ghar mein naya delivery package aana. Jab bhi naya item aayega, aap verify karoge ki purana kya tha aur naya kya aaya hai.

##### 3. **`ngOnInit()`** (Component Initialization)
* **What it does:** Component load hone ke baad sirf ek baar chalta hai. Is stage par inputs bind ho chuke hote hain. Yeh API call karne aur data variables set karne ke liye best place hai.
* **Hinglish Analogy:** Housewarming party. Ab inputs ready hain aur aap setup operations execute kar sakte ho.

##### 4. **`ngDoCheck()`** (Custom Change Detection)
* **What it does:** Har change detection cycle par yeh method run hota hai. Agar aapko koi aisi change detect karni hai jo Angular direct track nahi kar pata (jaise object mutations), toh aap yahan logic likhte ho.
* **Hinglish Analogy:** Security Guard checking. Har baar jab bhi click ya events honge, guard verify karega ki sab kuch normal hai ya nahi.

##### 5. **`ngAfterViewInit()`** (DOM templates ready)
* **What it does:** Jab component ka HTML aur uske saare child components DOM ke andar render ho jaate hain tab chalta hai. `@ViewChild` references is hook ke baad hi valid hote hain.
* **Hinglish Analogy:** Building construction certificate. Ab physical walls aur layouts full ready hain, aap direct inspections kar sakte ho.

##### 6. **`ngOnDestroy()`** (Teardown/Cleanup)
* **What it does:** Jab component screen/DOM se remove hone wala hota hai tab chalta hai. Memory leaks se bachne ke liye subscriptions, timers aur WebSocket links ko cancel karne ke liye iska use hota hai.
* **Hinglish Analogy:** Flat khali karna. Light-fan switch off karna aur locks check karna taaki baad mein bills (memory leak) na aayein.

#### 💻 Execution Sequence Code Example:
```typescript
import { 
  Component, Input, OnInit, OnChanges, DoCheck, 
  AfterViewInit, OnDestroy, SimpleChanges 
} from '@angular/core';

@Component({
  selector: 'app-lifecycle-logger',
  standalone: true,
  template: `<p>Active User: {{ user }}</p>`
})
export class LifecycleLoggerComponent implements OnInit, OnChanges, DoCheck, AfterViewInit, OnDestroy {
  @Input() user = '';

  constructor() {
    console.log('1. Constructor: Dependency resolved, inputs NOT ready.');
  }

  ngOnChanges(changes: SimpleChanges): void {
    console.log('2. ngOnChanges: Input reference updated:', changes);
  }

  ngOnInit(): void {
    console.log('3. ngOnInit: Component variables bound, fetching API data.');
  }

  ngDoCheck(): void {
    console.log('4. ngDoCheck: Change detection cycle check.');
  }

  ngAfterViewInit(): void {
    console.log('5. ngAfterViewInit: DOM view and child elements rendered.');
  }

  ngOnDestroy(): void {
    console.log('6. ngOnDestroy: Cleaning subscriptions and intervals.');
  }
}
```

> 💡 **Interviewer Focus:** Why network fetches belong in `ngOnInit` rather than the `constructor` (inputs are `undefined` in constructor), and preventing memory leaks in `ngOnDestroy`.


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
<details>
<summary><b>👀 Show Answer</b></summary>

* **One-Way Binding:** Data flows in a single direction.
  * **Component to View:** Interpolation `{{ value }}` or Property Binding `[property]="value"`.
  * **View to Component:** Event Binding `(event)="handler()"`.
* **Two-Way Binding:** Data flows in both directions simultaneously. Updates to the view (such as input entries) update the component class property, and modifications to the component class property update the DOM element. It is configured using the "banana-in-a-box" syntax `[(ngModel)]`.

#### 💬 Hinglish Analogy:
* **One-Way:** Bulletins on a notice board—you can only read updates (Component to View), or a drop-box where you submit a form (View to Component).
* **Two-Way:** A walkie-talkie conversation—dono directions mein message immediate aur continuous sync hota hai.

```html
<!-- One-Way Property + Event -->
<input [value]="username" (input)="username = $any($event.target).value">

<!-- Two-Way Binding (Equivalent) -->
<input [(ngModel)]="username">
```

> 💡 **Interviewer Focus:** Unidirectional data flow control and syntax equivalences behind the syntax wrapper of `[(ngModel)]`.

</details>
<hr/>

### ❓ Q12. **How does an Angular application bootstrap itself?**
<details>
<summary><b>👀 Show Answer</b></summary>

The bootstrapping process sets up the Angular environment and loads the root component:
1. **Entry Point (`angular.json`):** Points to the main file, usually `src/main.ts`.
2. **Bootstrapping Script (`main.ts`):** Calls `bootstrapApplication(AppComponent, config)` to launch the root component.
3. **Execution Context:** The compiler searches the HTML (`index.html`) for the root component selector (e.g., `<app-root></app-root>`) and renders the bootstrapped component within it.

```typescript
// main.ts (Modern Standalone Bootstrapping)
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));
```

> 💡 **Interviewer Focus:** Knowing the sequence from `angular.json` configuration, to the execution of `main.ts`, to the root template injection.

</details>
<hr/>

### ❓ Q13. **What is the purpose of the `tsconfig.json` file?**
<details>
<summary><b>👀 Show Answer</b></summary>

The **`tsconfig.json`** file configures the TypeScript compiler (`tsc`) options for compiling TS code into browser-compatible JavaScript.

#### ⚙️ Key Configurations in Angular:
* **`compilerOptions.strict`:** Enables strict type-checking flags (like `strictNullChecks`), preventing compile-time bugs.
* **`compilerOptions.target`:** Defines the output JavaScript target version (e.g., `es2022`).
* **`angularCompilerOptions`:** Configures Angular-specific template compiling checks (like `strictTemplates`, which enforces strict type checks on input bindings inside component templates).

> 💡 **Interviewer Focus:** Strict templates checking, output version targets, and compiler rule enforcement.

</details>
<hr/>

### ❓ Q14. **What is a Single Page Application (SPA)?**
<details>
<summary><b>👀 Show Answer</b></summary>

A **Single Page Application (SPA)** is a web application that loads only one HTML document (`index.html`) from the server. 

When the user navigates, the client-side router intercepts requests, dynamically updating the DOM rather than requesting new documents from the server. This prevents full-page refreshes, making transitions smooth and fast.

> 💡 **Interviewer Focus:** Client-side routing, intercepting anchor clicks, and updating parts of the DOM.

</details>
<hr/>

### ❓ Q15. **What is standard styling encapsulation in Angular?**
<details>
<summary><b>👀 Show Answer</b></summary>

Styling encapsulation determines how Angular scopes component styles to prevent them from leaking and affecting other components.

#### The Three Encapsulation Modes:
1. **`Emulated` (Default):** Angular intercepts component styles and adds unique attributes (like `_ngcontent-c1`) to selectors. This confines component styles to the component template without using the Shadow DOM.
2. **`ShadowDom`:** Angular uses the browser's native Shadow DOM API to isolate component markup and styles. Styles do not leak out, and global styles do not leak in.
3. **`None`:** Component styles are added directly to the document head as global styles.

```typescript
@Component({
  selector: 'app-scoped-card',
  encapsulation: ViewEncapsulation.Emulated, // Scopes styles locally
  styles: [`h3 { color: red; }`]
})
export class ScopedCardComponent {}
```

> 💡 **Interviewer Focus:** How Angular isolates styles under `Emulated` mode using generated HTML attributes, and when to use `ShadowDom` vs `None`.

</details>
<hr/>

### ❓ Q16. **What does the `@Injectable` decorator do?**
<details>
<summary><b>👀 Show Answer</b></summary>

The **`@Injectable`** decorator marks a class as a service that can be resolved by the Dependency Injection (DI) system.

It is **mandatory** if your service needs to inject other dependencies in its constructor. Without `@Injectable()`, Angular's DI compiler lacks the metadata needed to resolve and inject constructor arguments.

```typescript
@Injectable({
  providedIn: 'root' // Singleton registration
})
export class DataService {
  constructor(private http: HttpClient) {} // Requires @Injectable to resolve HttpClient
}
```

> 💡 **Interviewer Focus:** Emitting metadata parameter designs, constructor resolutions, and singleton scopes.

</details>
<hr/>

### ❓ Q17. **What is the difference between constructor parameter initialization and standard property assignments?**
<details>
<summary><b>👀 Show Answer</b></summary>

* **Constructor Parameter Initialization:** Runs when the JavaScript class is instantiated. It is used to resolve and inject dependencies (like services or `HttpClient`) via Dependency Injection:
  ```typescript
  constructor(private apiService: ApiService) {}
  ```
* **Standard Property Assignment:** Runs before the constructor executes. It initializes local class properties with default values:
  ```typescript
  title = 'My Workspace';
  ```

> 💡 **Interviewer Focus:** Dependency resolution timing vs standard property initialization.

</details>
<hr/>

### ❓ Q18. **What is npm and package.json?**
<details>
<summary><b>👀 Show Answer</b></summary>

* **npm (Node Package Manager):** A CLI utility and registry used to install, share, and manage third-party JavaScript libraries and packages in your project.
* **`package.json`:** A project configuration file that lists metadata, scripts (like `start`, `build`), and project dependencies with semantic version rules (e.g. dependencies vs devDependencies).

> 💡 **Interviewer Focus:** Understanding package installation workflows, locked version targets (`package-lock.json`), and script configurations.

</details>
<hr/>

### ❓ Q19. **What are the differences between HTML attributes and DOM properties?**
<details>
<summary><b>👀 Show Answer</b></summary>

* **HTML Attributes:** Defined in the HTML markup. They initialize DOM properties and their values are always strings (e.g., `value="John"`).
* **DOM Properties:** Represent properties on DOM nodes. They can be read and updated dynamically, and support complex types like booleans, arrays, or objects.

#### 💬 Hinglish Analogy:
* **HTML Attribute:** Car design specification sheets (static, set once at build/markup time).
* **DOM Property:** The actual car's state (dynamic, e.g. current speed or fuel level, which changes during execution).

> 💡 **Interviewer Focus:** Property binding targets DOM properties directly, which is why property binding supports complex data types while attributes only support string values.

</details>
<hr/>

### ❓ Q20. **What are components?**
<details>
<summary><b>👀 Show Answer</b></summary>

A **Component** is a class decorated with `@Component` that defines a reusable UI block in Angular. It combines:
1. **Class (TypeScript):** Manages the component's state and business logic.
2. **Template (HTML):** Defines the component's structure and layout.
3. **Styles (CSS/SCSS):** Defines the component's appearance.

> 💡 **Interviewer Focus:** Building blocks of Angular applications, combining visual layouts with local state logic.

</details>
<hr/>

### ❓ Q21. **How do you define input properties?**
<details>
<summary><b>👀 Show Answer</b></summary>

There are two ways to define inputs in Angular:
1. **Classic Decorator (`@Input()`):** Declares a property that a parent component can bind to:
   ```typescript
   @Input() userId: string = '';
   ```
2. **Modern Input Signal (`input()`):** Declares a read-only signal input (introduced in Angular 17.1+). This enables fine-grained change detection and compile-time validation:
   ```typescript
   userId = input<string>(''); // Returns a Signal
   ```

> 💡 **Interviewer Focus:** Decorator-based inputs vs Signal-based inputs, and how signals provide better type safety and change detection.

</details>
<hr/>

### ❓ Q22. **What are template expression bindings?**
<details>
<summary><b>👀 Show Answer</b></summary>

**Template expression bindings** evaluate expressions (such as variables, object lookups, or logic conditions) inside interpolation double braces `{{ expression }}`.

#### ⚠️ Rules and Constraints:
* Expressions must not have side effects (cannot use assignment operators like `=`, `+=`, or increment operators like `++`).
* Keep expressions simple. Do not call expensive methods inside template expressions, as they run on every change detection cycle, slowing down the application.

> 💡 **Interviewer Focus:** Execution frequency, avoiding side-effects, and keeping template bindings simple.

</details>
<hr/>

### ❓ Q23. **What is the standard workspace folder structure generated by the CLI?**
<details>
<summary><b>👀 Show Answer</b></summary>

* **`/src`**: Contains source code.
  * **`/app`**: Component, service, directive, and routing configuration files.
  * **`/assets`**: Static assets (images, fonts, JSON configuration files).
  * **`index.html`**: The single HTML page.
  * **`main.ts`**: The main application entry point.
* **`angular.json`**: CLI project configuration file.
* **`tsconfig.json`**: TypeScript compiler configuration file.
* **`package.json`**: Project scripts and dependency manifest.

> 💡 **Interviewer Focus:** Layout conventions, and where key build and environment settings live.

</details>
<hr/>

### ❓ Q24. **How do you define inline styles vs external style sheets in components?**
<details>
<summary><b>👀 Show Answer</b></summary>

* **Inline Styles:** Defined directly within the `@Component` decorator metadata using the `styles` array. Best for short, component-specific styles:
  ```typescript
  styles: [`h1 { font-weight: bold; }`]
  ```
* **External Stylesheets:** Point to external styling files (like `.css` or `.scss`) using the `styleUrls` (or `styleUrl` in modern versions) property:
  ```typescript
  styleUrl: './app.component.scss'
  ```

> 💡 **Interviewer Focus:** Knowing the style metadata options in the component decorator.

</details>
<hr/>

### ❓ Q25. **What are standalone dependencies?**
<details>
<summary><b>👀 Show Answer</b></summary>

**Standalone dependencies** are components, directives, or pipes that a standalone component imports directly in its `@Component` metadata:

```typescript
@Component({
  selector: 'app-nav',
  standalone: true,
  imports: [CommonModule, RouterModule, UserProfileComponent], // Standalone dependencies
  template: `<app-user-profile></app-user-profile>`
})
export class NavComponent {}
```

Unlike legacy applications, standalone components explicitly list their template dependencies, keeping components modular and easy to test.

> 💡 **Interviewer Focus:** Eliminating NgModules by declaring template dependencies directly at the component level.

</details>
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

Components can communicate in three main ways depending on their relationship in the component tree:

---

### 📥 1. Parent-to-Child Communication (Using Inputs)
* **Concept:** The parent component passes data down to the child component using property binding on the child's input properties (either using the classic `@Input()` decorator or modern `input()` signals).
* **💬 Hinglish Explanation:** Parent component child component ko metadata variables ya variables attributes data pass karta hai. Child component in inputs ko read kar sakta hai. Modern Angular mein signal-based inputs (`input()`) data checks ko aur simple bana dete hain.

#### 💻 Code Example:
```typescript
// child.component.ts (Child)
import { Component, Input, input } from '@angular/core';

@Component({
  selector: 'app-child-inputs',
  standalone: true,
  template: `
    <div class="box">
      <p>Classic Input Value: {{ username }}</p>
      <p>Signal Input Value: {{ age() }}</p>
    </div>
  `
})
export class ChildInputsComponent {
  // Classic decorator input
  @Input() username = '';

  // Modern Signal input (Read-only reactive signal)
  age = input<number>(0); 
}

// parent.component.ts (Parent)
import { Component } from '@angular/core';
import { ChildInputsComponent } from './child.component';

@Component({
  selector: 'app-parent-inputs',
  standalone: true,
  imports: [ChildInputsComponent],
  template: `
    <h2>Parent Component</h2>
    <!-- Passing data down via property bindings -->
    <app-child-inputs [username]="currentAdmin" [age]="adminAge"></app-child-inputs>
  `
})
export class ParentInputsComponent {
  currentAdmin = 'Alice Smith';
  adminAge = 28;
}
```

---

### 📤 2. Child-to-Parent Communication (Using Outputs & EventEmitters)
* **Concept:** The child component notifies the parent component about events or interactions by emitting an event using an `@Output()` property combined with `EventEmitter` (or the modern `output()` function). The parent listens to this event in its template.
* **💬 Hinglish Explanation:** Child component parent component ko messages/events trigger karke updates data return bhejta hai. Jaise child component ka submit button click hone par event emit hota hai, aur parent component use listen karke function run karta hai.

#### 💻 Code Example:
```typescript
// child.component.ts (Child)
import { Component, Output, EventEmitter, output } from '@angular/core';

@Component({
  selector: 'app-child-outputs',
  standalone: true,
  template: `
    <button (click)="triggerAlert()">Notify Parent (Classic)</button>
    <button (click)="triggerSignalAlert()">Notify Parent (Modern)</button>
  `
})
export class ChildOutputsComponent {
  // Classic Output
  @Output() alert = new EventEmitter<string>();

  // Modern Output API
  signalAlert = output<string>();

  triggerAlert() {
    this.alert.emit('Classic Event Triggered!');
  }

  triggerSignalAlert() {
    this.signalAlert.emit('Modern Output Event Triggered!');
  }
}

// parent.component.ts (Parent)
import { Component } from '@angular/core';
import { ChildOutputsComponent } from './child.component';

@Component({
  selector: 'app-parent-outputs',
  standalone: true,
  imports: [ChildOutputsComponent],
  template: `
    <h2>Parent listener</h2>
    <!-- Listening to event bindings emitted by child -->
    <app-child-outputs 
      (alert)="onAlertReceived($event)"
      (signalAlert)="onAlertReceived($event)">
    </app-child-outputs>
  `
})
export class ParentOutputsComponent {
  onAlertReceived(message: string) {
    console.log(`Parent received message: ${message}`);
  }
}
```

---

### 🌐 3. Unrelated Components Communication (Using Shared Services)
* **Concept:** When components do not share a parent-child relationship, they communicate by injecting a shared singleton service. The service exposes a stream (using RxJS `BehaviorSubject`) or a reactive Angular `Signal` that components can subscribe/bind to.
* **💬 Hinglish Explanation:** Agar do components bilkul alag hain (unrelated), toh wo direct dynamic communication nahi kar sakte. Unke liye ek shared common service banayi jaati hai (providedIn: 'root' ke saath). Ek component service ki state change karta hai aur doosra component use auto-receive (subscribe/read) kar leta hai.

#### 💻 Code Example:
```typescript
// theme.service.ts (Shared Service)
import { Injectable, signal } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  // Option A: Signals (Modern)
  themeSignal = signal<'light' | 'dark'>('light');

  // Option B: RxJS BehaviorSubject (Classic)
  private themeSubject = new BehaviorSubject<'light' | 'dark'>('light');
  theme$ = this.themeSubject.asObservable();

  toggleTheme() {
    const nextTheme = this.themeSignal() === 'light' ? 'dark' : 'light';
    this.themeSignal.set(nextTheme);
    this.themeSubject.next(nextTheme);
  }
}

// component-a.component.ts (Updates State)
import { Component } from '@angular/core';
import { ThemeService } from './theme.service';

@Component({
  selector: 'app-comp-a',
  standalone: true,
  template: `<button (click)="themeService.toggleTheme()">Toggle System Theme</button>`
})
export class ComponentA {
  // Inject service via constructor
  constructor(public themeService: ThemeService) {}
}

// component-b.component.ts (Reads State)
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ThemeService } from './theme.service';

@Component({
  selector: 'app-comp-b',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div [class]="currentThemeSignal()">
      <p>Active Theme (Signal): {{ currentThemeSignal() }}</p>
      <p>Active Theme (RxJS): {{ themeService.theme$ | async }}</p>
    </div>
  `
})
export class ComponentB {
  currentThemeSignal;
  
  // Inject service via constructor and map the signal
  constructor(public themeService: ThemeService) {
    this.currentThemeSignal = this.themeService.themeSignal;
  }
}
```

> 💡 **Interviewer Focus:** Input/Output pipelines, structural hierarchies traversal rules, and using centralized services vs local bindings for state isolation.


</details>
<hr/>

### ❓ Q29. **What is a Pipe, and what is the difference between a Pure and an Impure Pipe?**
<details>
<summary><b>👀 Show Answer</b></summary>

### 📌 1. Pipe Kya Hai? (What is a Pipe?)
Angular me **Pipe** ek simple tarika hai template HTML me dynamic data ko format karke represent karne ka. Ye actual value ko backend me change nahi karta, sirf user ko look-and-feel badal ke dikhata hai.
* **Syntax:** `{{ rawData | pipeName : arguments }}`
* **Example:** `{{ 'hello world' | uppercase }}` transforms to `HELLO WORLD`.

---

### 🎭 2. Real-Life Analogy: Lallan (Pure) vs Babban (Impure)

* **Pure Pipe (Smart & Lazy Lallan):** 
  * Lallan ek smart ladka hai jo memory/caching ka use karta hai. Agar aapne isse pucha: *"Tell the length of 'Apple'"*, ye calculate karke bolega *"5"* aur ise brain me save (cache) kar lega.
  * Agar aap isse 10 bar aur puchoge *"Tell the length of 'Apple'"*, ye recalculate nahi karega, balki turant memory se *"5"* bol dega.
  * Lallan tabhi dobara dimaag chalayega jab input change ho (jaise aapne pucha *"Mango"*).
* **Impure Pipe (Anxious Babban):** 
  * Babban bahut hi hyperactive aur anxious hai. Agar aapne isse pucha: *"Tell the length of 'Apple'"*, ye calculate karke bolega *"5"*.
  * Lekin Babban har second, har mouse movement par, ya page pe kahi bhi click karne par, bar-bar calculate karta rahega ki *"Apple ka length 5 hi hai na?"*. Isse system CPU overload ho jata hai.

---

### ⚔️ 3. Pure vs Impure Pipes (Core Comparison)

| Parameter | Pure Pipe (Default) | Impure Pipe (`pure: false`) |
|---|---|---|
| **Trigger Rule** | Tabhi execute hota hai jab input ka **Reference Change** ho. | Har **Change Detection Cycle** (click, keypress, API response, mouse scroll) par execute hota hai. |
| **Caching / Memoization** | **Yes.** Previous output ko store rakhta hai agar input same ho. | **No.** Har baar fresh calculation karta hai. |
| **Use Case** | Formatting dates, currency, numbers, text transforms (strings, numbers, booleans). | Jab array ya object ke andar ki details mutate ho rahi hon bina reference badle (e.g., `list.push(item)`). |
| **Performance** | **Very High Performance** 🚀 (Very lightweight). | **Poor Performance** ⚠️ (Can freeze the UI if doing heavy calculations). |

---

### 💻 4. Code Implementation Example

#### Option A: Pure Pipe (Default behaviour)
Agar aap pure pipe me array pass karoge aur array me `.push()` se naya item add karoge, toh Pure Pipe run **nahi** hoga, kyunki array ka reference change nahi hua.

```typescript
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'searchFilter',
  pure: true, // Default true hota hai
  standalone: true
})
export class SearchFilterPipe implements PipeTransform {
  transform(items: string[], searchText: string): string[] {
    console.log('Pure Pipe executed!'); // Tabhi chalega jab list ya text ka dynamic reference badlega
    if (!items || !searchText) return items;
    return items.filter(item => item.toLowerCase().includes(searchText.toLowerCase()));
  }
}
```
* **Why it won't update on mutation:**
  ```typescript
  // Component code:
  items = ['Apple', 'Banana'];
  
  addItem() {
    this.items.push('Mango'); // Pure pipe will NOT execute because array reference is same!
    // isko chalane ke liye reference badalna padega: 
    // this.items = [...this.items, 'Mango'];
  }
  ```

#### Option B: Impure Pipe (`pure: false`)
Impure pipe check karega ki array ke andar koi elements push huye hain ya nahi, chahe reference same hi kyun na ho.

```typescript
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'searchFilterImpure',
  pure: false, // ⚠️ Impure banata hai
  standalone: true
})
export class SearchFilterImpurePipe implements PipeTransform {
  transform(items: string[], searchText: string): string[] {
    console.log('Impure Pipe executed on every tick!'); // Har event/click par chalega
    if (!items || !searchText) return items;
    return items.filter(item => item.toLowerCase().includes(searchText.toLowerCase()));
  }
}
```
* **Why it updates on mutation:**
  ```typescript
  // Component code:
  items = ['Apple', 'Banana'];
  
  addItem() {
    this.items.push('Mango'); // Impure pipe WILL execute and show Mango instantly!
  }
  ```

---

### ⚠️ Impure Pipes Performance Alert!
Impure pipes ko build karte waqt humesha dhyan rakhe ki isme heavy looping ya heavy calculations na ho. Agar aapne ek bada array filter impure pipe me daal diya, toh har cursor click/mouse hover par browser slow ho jayega.

> 💡 **Interviewer Focus:** Input reference caching, change detection cycles, why standard filter pipes are generally avoided in Angular (instead using component-level logic or signals), and the performance footprint of impure pipes.

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

### ❓ Q34. **How does `HttpClient` handle error propagation using RxJS `catchError`?**
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
<details>
<summary><b>👀 Show Answer</b></summary>

* **Element Bindings:** Bind properties or events of elements *within* the component's own template (e.g., `<button [disabled]="isDisabled">`).
* **Host Bindings:** Bind properties or listen to events of the **host element** itself (the element on which the component or directive is declared). This is managed using the `@HostBinding` and `@HostListener` decorators or the `host` configuration property in modern metadata.

```typescript
@Directive({
  selector: '[appActive]',
  standalone: true,
  host: {
    '[class.active]': 'isActive', // Host property binding
    '(click)': 'toggleActive()' // Host event listener
  }
})
export class ActiveDirective {
  isActive = false;
  toggleActive() { this.isActive = !this.isActive; }
}
```

> 💡 **Interviewer Focus:** Understanding styling encapsulation, host interaction scopes, and modern metadata binding declarations.

</details>
<hr/>

### ❓ Q36. **Explain what routing guards do.**
<details>
<summary><b>👀 Show Answer</b></summary>

**Route Guards** run code before navigation completes to determine if a route transition is allowed to proceed (e.g., to prevent anonymous users from accessing private pages).

#### 🛡️ Modern Functional Guards:
In modern Angular, guards are defined as functions (like `CanActivateFn`) rather than classes:

```typescript
export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  
  if (authService.isLoggedIn()) {
    return true;
  }
  
  return router.parseUrl('/login'); // Redirect
};
```

> 💡 **Interviewer Focus:** Route interception lifecycle, authorization checks, and dynamic redirection returning UrlTree values.

</details>
<hr/>

### ❓ Q37. **How do you pass queries and query parameters?**
<details>
<summary><b>👀 Show Answer</b></summary>

* **Setting Query Parameters:** Pass query parameters using the `queryParams` property in `routerLink` or programmatically via the `Router` service:
  ```html
  <a [routerLink]="['/products']" [queryParams]="{ category: 'shoes' }">Shoes</a>
  ```
* **Reading Query Parameters:** Inject **`ActivatedRoute`** and subscribe to the `queryParamMap` observable:
  ```typescript
  route = inject(ActivatedRoute);
  category$ = this.route.queryParamMap.pipe(map(params => params.get('category')));
  ```

> 💡 **Interviewer Focus:** Observable param flows, reading query string tokens, and passing options programmatically.

</details>
<hr/>

### ❓ Q38. **What is the purpose of HTTP interceptors?**
<details>
<summary><b>👀 Show Answer</b></summary>

**HTTP Interceptors** run code to inspect and modify outgoing requests and incoming responses globally. 

#### Common Use Cases:
* Appending Authorization tokens (like JWT) in headers.
* Intercepting network errors (like 401s) to trigger silent token refreshes.
* Injecting default base backend URLs.
* Managing load spinners and tracking progress dynamically.

> 💡 **Interviewer Focus:** Global request pipeline control, header injection, and functional interceptor architecture.

</details>
<hr/>

### ❓ Q39. **How do you manage nested route setups?**
<details>
<summary><b>👀 Show Answer</b></summary>

Nested (child) routes let you render parent pages containing nested subviews. They are configured using the **`children`** array in route definitions. 

The parent component template must declare a **`<router-outlet></router-outlet>`** where the active child component is rendered.

```typescript
export const routes: Route[] = [{
  path: 'settings',
  component: SettingsComponent,
  children: [
    { path: 'profile', component: ProfileSettingsComponent },
    { path: 'security', component: SecuritySettingsComponent }
  ]
}];
```

> 💡 **Interviewer Focus:** Nested layout design, path inheritance, and using child router outlets.

</details>
<hr/>

### ❓ Q40. **What is the difference between a custom directive and standard component?**
<details>
<summary><b>👀 Show Answer</b></summary>

* **Standard Component:** Represents a complete layout component with its own visual template and styling. Used to build independent, reusable UI views (like `<app-sidebar>`).
* **Custom Directive:** Class with no template. It attaches custom styling or behavior to an **existing element** (like custom validation checks or hover color changes).

> 💡 **Interviewer Focus:** Visual layouts (components) vs enriching existing DOM element behaviors (directives).

</details>
<hr/>

### ❓ Q41. **Explain the `trackBy` function for template lists.**
<details>
<summary><b>👀 Show Answer</b></summary>

When rendering a list using `*ngFor`, Angular checks item identity references to update the DOM. If you update the list array reference, Angular destroys and recreates all DOM nodes by default, which can cause lag.

Providing a **`trackBy`** function tells Angular to track items by a custom unique identifier (like an `id` or index) rather than their reference. This allows Angular to update only modified items in the DOM, keeping rendering fast.

```typescript
trackByProductId(index: number, product: Product): number {
  return product.id; // Tracks items by ID
}
```
**In HTML:**
```html
<li *ngFor="let p of products; trackBy: trackByProductId">{{ p.name }}</li>
```

> 💡 **Interviewer Focus:** Minimizing DOM updates, list rendering performance, and how modern built-in control flow `@for` handles this natively.

</details>
<hr/>

### ❓ Q42. **What is view encapsulation and what is its default mode?**
<details>
<summary><b>👀 Show Answer</b></summary>

**View Encapsulation** scopes component styles to prevent them from leaking out and affecting other parts of the application. 

Its default mode is **`ViewEncapsulation.Emulated`**, which scopes styles locally by generating unique attributes (like `_nghost-c0` and `_ngcontent-c0`) on elements at compile time.

> 💡 **Interviewer Focus:** Knowing the default mode (`Emulated`) and how compiled HTML attributes isolate style boundaries.

</details>
<hr/>

### ❓ Q43. **How do you share state using simple services?**
<details>
<summary><b>👀 Show Answer</b></summary>

To share state between components using a service, configure a root injectable service containing a private state variable and expose it via public methods or reactive streams:

1. **Signals Approach (Modern):** Expose read-only signals and mutate values using methods:
   ```typescript
   private stateSignal = signal<User | null>(null);
   user = this.stateSignal.asReadonly();
   updateUser(u: User) { this.stateSignal.set(u); }
   ```
2. **RxJS Approach:** Use a `BehaviorSubject` to multicast state updates to subscribers:
   ```typescript
   private state$ = new BehaviorSubject<User | null>(null);
   user$ = this.state$.asObservable();
   updateUser(u: User) { this.state$.next(u); }
   ```

> 💡 **Interviewer Focus:** Decoupling state logic from views, and exposing data reactively via Signals or RxJS observables.

</details>
<hr/>

### ❓ Q44. **What is the difference between a Subject and a BehaviorSubject?**
<details>
<summary><b>👀 Show Answer</b></summary>

* **`Subject`:** Does not hold a state value. It acts as an event emitter, sending values to active subscribers only. New subscribers do not receive past values.
* **`BehaviorSubject`:** Holds a state value and requires an initial value. It caches its latest emitted value, sending it to new subscribers immediately upon subscription. You can read its current value synchronously at any time using `.value` or `.getValue()`.

> 💡 **Interviewer Focus:** State management vs event streams, and initial value requirements.

</details>
<hr/>

### ❓ Q45. **What are standalone components dependencies routing?**
<details>
<summary><b>👀 Show Answer</b></summary>

Standalone components configure routing dependencies directly in their route setup. 

Instead of registering routing modules, routes are passed directly to `provideRouter()` during bootstrapping. Individual route destinations load dynamically using the `loadComponent` dynamic import syntax.

```typescript
export const appRoutes: Route[] = [
  {
    path: 'dashboard',
    loadComponent: () => import('./dashboard/dashboard.component').then(m => m.DashboardComponent)
  }
];
```

> 💡 **Interviewer Focus:** Dynamic imports, lazy-loading standalone targets, and bootstrapping routing without `RouterModule`.

</details>
<hr/>

### ❓ Q46. **What is the difference between view providers and standard providers?**
<details>
<summary><b>👀 Show Answer</b></summary>

* **`providers`**: Dependencies are available to the component, its template, and all child components projected into it via `<ng-content>`.
* **`viewProviders`**: Dependencies are restricted to the component and its template views. Children projected via `<ng-content>` cannot access these dependencies, preserving encapsulation boundaries.

> 💡 **Interviewer Focus:** Restricting dependency access scopes in projected content.

</details>
<hr/>

### ❓ Q47. **How do you resolve dynamic resources using route resolvers?**
<details>
<summary><b>👀 Show Answer</b></summary>

A **Route Resolver** fetches data *before* navigation completes, ensuring page transitions only occur once the necessary data is loaded.

#### ⚙️ Modern Functional Resolver:
```typescript
export const productResolver: ResolveFn<Product> = (route, state) => {
  const api = inject(ProductService);
  const id = route.paramMap.get('id')!;
  return api.getProductDetails(id); // Router blocks until this emits
};
```
**Route Registration:**
```typescript
{ path: 'product/:id', component: ProductComponent, resolve: { product: productResolver } }
```

> 💡 **Interviewer Focus:** Data pre-loading, routing lifecycles, and functional resolver designs.

</details>
<hr/>

### ❓ Q48. **What is the purpose of custom directives?**
<details>
<summary><b>👀 Show Answer</b></summary>

Custom directives attach styling, layout modifications, or behavior to elements dynamically. They make code dry by encapsulating common DOM interactions:

```typescript
@Directive({ selector: '[appAutoCollapse]', standalone: true })
export class AutoCollapseDirective {
  @HostListener('mouseleave') onLeave() {
    // Perform collapse animation logic on the host element
  }
}
```

> 💡 **Interviewer Focus:** Encapsulating common element behaviors to make templates cleaner and more reusable.

</details>
<hr/>

### ❓ Q49. **How do you handle event bubbling inside HostListeners?**
<details>
<summary><b>👀 Show Answer</b></summary>

To prevent event bubbling (propagation up the DOM tree) within a `@HostListener`, capture the event object (using `$event`) in the decorator arguments and call **`stopPropagation()`** or **`preventDefault()`** directly inside the handler method:

```typescript
@HostListener('click', ['$event'])
onClick(event: Event) {
  event.stopPropagation(); // Stops event bubbling up to parent nodes
}
```

> 💡 **Interviewer Focus:** Capturing the event object dynamically in decorators, and managing event propagation.

</details>
<hr/>

### ❓ Q50. **What is the difference between dynamic and static components?**
<details>
<summary><b>👀 Show Answer</b></summary>

* **Static Components:** Declared directly in component templates using selector tags (e.g. `<app-header></app-header>`). They are instantiated and destroyed automatically by Angular.
* **Dynamic Components:** Instantiated programmatically at runtime. You use a container reference (**`ViewContainerRef`**) to inject and instantiate components on-demand (e.g., dynamically displaying custom alerts or modals based on API conditions).

```typescript
@Component({ ... })
export class ModalWrapperComponent {
  container = inject(ViewContainerRef);

  loadModal() {
    this.container.clear();
    const componentRef = this.container.createComponent(ModalComponent);
    componentRef.instance.message = 'Dynamic Modal Loaded!';
  }
}
```

> 💡 **Interviewer Focus:** Programmatic view generation, using `ViewContainerRef`, and managing dynamic component references.

</details>
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
<details>
<summary><b>👀 Show Answer</b></summary>

To dynamically change validator constraints at runtime:
1. Access the specific control reference.
2. Call **`setValidators([...])`** (or `clearValidators()`) to configure new constraints.
3. Call **`updateValueAndValidity()`** to force the control to re-evaluate its state and status.

```typescript
updateValidation(isRequired: boolean) {
  const emailControl = this.profileForm.get('email')!;
  
  if (isRequired) {
    emailControl.setValidators([Validators.required, Validators.email]);
  } else {
    emailControl.clearValidators();
  }
  
  emailControl.updateValueAndValidity(); // Forces re-validation
}
```

> 💡 **Interviewer Focus:** Runtime validator changes, cleaning filters, and calling `updateValueAndValidity()`.

</details>
<hr/>

### ❓ Q61. **Explain the difference between `throttleTime` and `debounceTime`.**
<details>
<summary><b>👀 Show Answer</b></summary>

* **`debounceTime(X)`:** Delays emissions from the source observable. It only emits a value if a specified window of time (X milliseconds) passes without any new emissions.
  * *Use Case:* Search boxes. Prevents making API calls while the user is still typing.
* **`throttleTime(X)`:** Emits the first value, then ignores subsequent values for a specified window of time (X milliseconds).
  * *Use Case:* Click limits. Prevents double-clicking a submit button by ignoring consecutive clicks.

> 💡 **Interviewer Focus:** Event rate limits, search optimizations, and button click protection.

</details>
<hr/>

### ❓ Q62. **What are Route Guards resolvers and how do they differ from guards?**
<details>
<summary><b>👀 Show Answer</b></summary>

* **Route Guards (`CanActivateFn`):** Determine *if* a user can access a route (returns `true` or `false`/`UrlTree`). They do not load data; they simply block or allow access.
* **Route Resolvers (`ResolveFn`):** Fetch data *before* navigation completes. If the user is allowed to access the route, the resolver fetches the data, passing it to the routed component so it is available immediately upon load.

> 💡 **Interviewer Focus:** Navigation blocking (guards) vs pre-loading data (resolvers).

</details>
<hr/>

### ❓ Q63. **How do you configure micro-frontend federations?**
<details>
<summary><b>👀 Show Answer</b></summary>

Micro-frontend federation allows a shell application to load compiled components from remote applications at runtime:

1. **Build Tool Configuration (`webpack.config` or `esbuild` configurations):** Use `@angular-architects/module-federation` to configure the host (shell) and remotes:
   * **Host:** Maps remote entry URLs to scope keys.
   * **Remotes:** Expose entry files containing lazy-loaded components or routing definitions.
2. **Dynamic Route Configurations:** Load remote components on-demand using the router:
   ```typescript
   {
     path: 'dashboard',
     loadChildren: () => loadRemoteModule({
       type: 'module',
       remoteEntry: 'http://localhost:4201/remoteEntry.js',
       exposedModule: './DashboardModule'
     }).then(m => m.DashboardModule)
   }
   ```

> 💡 **Interviewer Focus:** Decoupled deployment pipelines, using `loadRemoteModule`, and sharing common dependencies.

</details>
<hr/>

### ❓ Q64. **Explain what the NgRx Effects pattern handles.**
<details>
<summary><b>👀 Show Answer</b></summary>

In NgRx, components dispatch Actions to update state. However, components should not handle side effects (like HTTP requests or storage actions) directly.

The **NgRx Effects** pattern handles asynchronous operations outside components:
1. An Effect listens for specific **Actions** dispatched to the store.
2. It performs the asynchronous operation (such as calling a backend service).
3. Once the operation completes, the Effect dispatches a **new Action** (containing the success payload or error) to update the store via Reducers.

This keeps components thin and focused strictly on rendering UI templates.

> 💡 **Interviewer Focus:** Decoupling side effects from components, routing actions, and using RxJS streams to update the store.

</details>
<hr/>

### ❓ Q65. **How do you implement optimistic UI updates using state management?**
<details>
<summary><b>👀 Show Answer</b></summary>

An **optimistic UI update** updates the UI state immediately under the assumption that the backend operation will succeed, making the application feel faster.

#### ⚙️ Implementation Workflow:
1. The user triggers an action (like liking a post).
2. The UI state updates immediately, and the component starts the backend API request.
3. **If the request succeeds:** Do nothing. The UI state is already correct.
4. **If the request fails:** The catch block intercepts the error, rolls back the state change to its previous value, and displays an error message.

```typescript
likePost(postId: number) {
  const previousState = this.store.posts();
  
  // 1. Optimistic Update (immediate UI update)
  this.store.setLiked(postId, true);

  // 2. Call backend
  this.api.likePost(postId).subscribe({
    error: () => {
      // 3. Rollback on failure
      this.store.setPosts(previousState);
      this.toast.error('Failed to save like. Please try again.');
    }
  });
}
```

> 💡 **Interviewer Focus:** Improving perceived performance, caching previous state, and handling rollbacks.

</details>
<hr/>

### ❓ Q66. **What is structural directives context?**
<details>
<summary><b>👀 Show Answer</b></summary>

Structural directives (like `*ngIf` or `*ngFor`) use a **context object** to pass values from the directive to the template variables declared in the host element.

For example, when writing `let item of items`, the directive instantiates the template with a context object. The object uses the **`$implicit`** property to bind default values, and named properties to bind other values (like `index` or `first` in `*ngFor` loops).

```typescript
// Custom structural directive passing context data
this.viewContainer.createEmbeddedView(this.templateRef, {
  $implicit: 'Default Value',
  index: 0
});
```

> 💡 **Interviewer Focus:** Template variables rendering, binding custom fields, and using `$implicit`.

</details>
<hr/>

### ❓ Q67. **How do you configure cross-origin resource sharing (CORS) locally?**
<details>
<summary><b>👀 Show Answer</b></summary>

CORS issues occur when your frontend (e.g. `http://localhost:4200`) requests resources from a backend running on a different domain or port (e.g. `http://localhost:8080`) during development.

To bypass CORS locally, configure an Angular dev proxy:
1. Create a `proxy.conf.json` file in the root of your workspace:
   ```json
   {
     "/api": {
       "target": "http://localhost:8080",
       "secure": false,
       "changeOrigin": true
     }
   }
   ```
2. Register the proxy file in `angular.json` under the serve architect options:
   ```json
   "serve": {
     "options": {
       "proxyConfig": "proxy.conf.json"
     }
   }
   ```
3. Update your HTTP calls to use relative paths (e.g., `/api/users`), which the dev server will route to the backend target.

> 💡 **Interviewer Focus:** Dev proxies, path rewrites, and target server routing.

</details>
<hr/>

### ❓ Q68. **What is the difference between dynamic imports and standard imports?**
<details>
<summary><b>👀 Show Answer</b></summary>

* **Standard Imports (`import { X } from './module'`):** Evaluated at compile time. The imported code is included in the main bundle and loaded immediately when the application starts, even if it is not used.
* **Dynamic Imports (`import('./module')`):** Evaluated at runtime. Next.js/Webpack splits the imported code into a separate chunk, loading it over the network only when the import function is executed. This is standard in lazy-loaded routes and components.

> 💡 **Interviewer Focus:** Bundle splitting, reducing initial load times, and dynamic compilation.

</details>
<hr/>

### ❓ Q69. **Explain change detection tree checks optimizations.**
<details>
<summary><b>👀 Show Answer</b></summary>

To prevent performance issues from frequent change detection checks:
1. **Use `ChangeDetectionStrategy.OnPush`:** Skips checking component subtrees unless their inputs receive new references.
2. **Run Code Outside Angular (`NgZone.runOutsideAngular`):** Runs tasks (like animations, Canvas redraws, or mouse movement listeners) without triggering change detection:
   ```typescript
   this.ngZone.runOutsideAngular(() => {
     // High-frequency task runs here without triggering change detection
   });
   ```
3. **Use Signals:** Enables fine-grained reactivity, allowing Angular to update only modified DOM nodes directly without traversing the entire component tree.

> 💡 **Interviewer Focus:** Fine-grained reactivity, using `runOutsideAngular` to run tasks outside Angular's zone, and `OnPush` performance strategies.

</details>
<hr/>

### ❓ Q70. **What is compile-time lazy loading?**
<details>
<summary><b>👀 Show Answer</b></summary>

**Compile-time lazy loading** is code-splitting configured during compilation. 

The compiler identifies dynamic imports (e.g., in router configurations like `loadComponent: () => import('./profile')`) and builds them into separate JavaScript files. 

These files are not included in the main bundle, and are loaded by the browser only when the user navigates to those specific routes.

> 💡 **Interviewer Focus:** Code-splitting rules, router integrations, and improving initial load times.

</details>
<hr/>

### ❓ Q71. **How do you configure custom route strategies?**
<details>
<summary><b>👀 Show Answer</b></summary>

Angular destroys the active component when navigating away from a route. If a user returns to that route, Angular creates a new instance of the component from scratch.

To preserve component state across navigations (e.g., to prevent destroying a dashboard view), implement a custom **`RouteReuseStrategy`**:

```typescript
import { RouteReuseStrategy, ActivatedRouteSnapshot, DetachedRouteHandle } from '@angular/router';

export class CustomRouteReuseStrategy implements RouteReuseStrategy {
  private handlers: { [key: string]: DetachedRouteHandle } = {};

  shouldDetach(route: ActivatedRouteSnapshot): boolean { return true; } // Cache this route
  store(route: ActivatedRouteSnapshot, handle: DetachedRouteHandle): void {
    this.handlers[route.routeConfig?.path || ''] = handle; // Save instance
  }
  shouldAttach(route: ActivatedRouteSnapshot): boolean {
    return !!this.handlers[route.routeConfig?.path || ''];
  }
  retrieve(route: ActivatedRouteSnapshot): DetachedRouteHandle | null {
    return this.handlers[route.routeConfig?.path || ''] || null;
  }
  shouldReuseRoute(future: ActivatedRouteSnapshot, curr: ActivatedRouteSnapshot): boolean {
    return future.routeConfig === curr.routeConfig;
  }
}
```

Register your custom strategy in `app.config.ts`:
```typescript
providers: [{ provide: RouteReuseStrategy, useClass: CustomRouteReuseStrategy }]
```

> 💡 **Interviewer Focus:** Caching components to preserve state across navigations, and implementing `RouteReuseStrategy` methods.

</details>
<hr/>

### ❓ Q72. **What is the difference between `valueChanges` and `statusChanges`?**
<details>
<summary><b>👀 Show Answer</b></summary>

* **`valueChanges`:** An RxJS observable that emits a value whenever a form control's value changes (such as keyboard entries in input fields).
* **`statusChanges`:** An RxJS observable that emits a validation status (e.g., `VALID`, `INVALID`, `PENDING`, or `DISABLED`) whenever control validation runs.

```typescript
this.profileForm.get('email')!.statusChanges.subscribe(status => {
  console.log(`Email validation status is: ${status}`);
});
```

> 💡 **Interviewer Focus:** Forms streams, tracking input values vs tracking validation states.

</details>
<hr/>

### ❓ Q73. **How do you mock HTTP services in unit tests?**
<details>
<summary><b>👀 Show Answer</b></summary>

To test services that make HTTP requests without hitting real servers, mock `HttpClient` using **`provideHttpClientTesting()`** and the **`HttpTestingController`**:

```typescript
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';

describe('DataService', () => {
  let service: DataService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [DataService, provideHttpClient(withInterceptors([])), provideHttpClientTesting()]
    });
    service = TestBed.inject(DataService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('should fetch users via GET', () => {
    service.getUsers().subscribe(users => {
      expect(users.length).toBe(2);
    });

    const req = httpMock.expectOne('/api/users');
    expect(req.request.method).toBe('GET');
    req.flush([{ id: 1, name: 'Alice' }, { id: 2, name: 'Bob' }]); // Mock response
  });

  afterEach(() => httpMock.verify()); // Confirm no outstanding HTTP calls
});
```

> 💡 **Interviewer Focus:** Mocking network responses using `HttpTestingController`, using `.flush()`, and calling `.verify()` to prevent request leaks.

</details>
<hr/>

### ❓ Q74. **What is tree-shaking compilation?**
<details>
<summary><b>👀 Show Answer</b></summary>

**Tree-shaking** is a build step that analyzes your import dependency graphs to identify and remove unused code from your production bundle. 

It relies on static analysis of ES6 modules (using `import` and `export` statements). In Angular, using standalone components and root injectables enables tree-shaking, keeping production JavaScript bundle sizes small.

> 💡 **Interviewer Focus:** Static code analysis, dead code elimination, and code modularity.

</details>
<hr/>

### ❓ Q75. **How do you configure content projection slots?**
<details>
<summary><b>👀 Show Answer</b></summary>

Multi-slot content projection allows you to inject different pieces of content from a parent component into specific slots within a child component template.

To configure slots, add the **`select`** attribute to `<ng-content>` tags inside the child component template. The `select` attribute can target CSS selectors, class names, or attributes:

```html
<!-- Child Component Template (app-card) -->
<div class="card">
  <div class="header">
    <ng-content select="[card-header]"></ng-content>
  </div>
  <div class="body">
    <ng-content></ng-content> <!-- Catch-all slot -->
  </div>
</div>

<!-- Parent Component Usage -->
<app-card>
  <h2 card-header>Profile Details</h2> <!-- Injected into header slot -->
  <p>Some profile text content...</p> <!-- Injected into catch-all slot -->
</app-card>
```

> 💡 **Interviewer Focus:** Multi-slot projection setups, selecting slots using attributes/CSS classes, and DOM injection layouts.

</details>
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

### ❓ Q84. **Explain how to prevent `ExpressionChangedAfterItHasBeenCheckedError`.**
<details>
<summary><b>👀 Show Answer</b></summary>

This error occurs in **Development Mode** because Angular performs a verification pass after a change detection run to ensure that the view matches the model. 

If a value (such as a shared service status or component property) changes between the change detection pass and the verification pass, Angular throws this error to warn you of inconsistent state.

#### 🛠️ Common Solutions:
1. **Shift Updates to a Safe Lifecycle Hook:** Do not update bound values in DOM-centric hooks (like `ngAfterViewInit` or `ngAfterContentInit`). Update values in `ngOnInit` instead, before rendering finishes.
2. **Defer State Updates:** Wrap updates in a asynchronous task (using `setTimeout` or `Promise.resolve().then()`) to push them to the next JavaScript event loop tick:
   ```typescript
   setTimeout(() => this.isActive = true);
   ```
3. **Inject ChangeDetectorRef:** Manually call `detectChanges()` to force change detection to run:
   ```typescript
   this.cdr.detectChanges();
   ```

> 💡 **Interviewer Focus:** Rendering lifecycles, development vs production verification passes, and using asynchronous microtasks to defer updates.

</details>
<hr/>

### ❓ Q85. **What is dynamic route compilation?**
<details>
<summary><b>👀 Show Answer</b></summary>

**Dynamic Route Compilation** is a runtime process where the router loads route configurations on-demand (e.g., from a database or remote micro-frontend config) rather than using a static, hardcoded route tree during compilation:

```typescript
const routes: Route[] = [
  {
    path: 'features',
    loadChildren: () => fetch('/api/dynamic-routes')
      .then(res => res.json())
      .then(config => parseRoutes(config))
  }
];
```

This is crucial for enterprise systems where user permissions determine which routing options are available at runtime.

> 💡 **Interviewer Focus:** Fetching routes dynamically from databases, dynamic route mapping, and access control.

</details>
<hr/>

### ❓ Q86. **How do you configure custom decorators in Angular?**
<details>
<summary><b>👀 Show Answer</b></summary>

Custom decorators are factory functions that return a decorator function. They wrap and modify the behavior of classes, properties, or methods.

#### ⚙️ Example: Custom Method Log Decorator:
```typescript
export function LogMethod(): MethodDecorator {
  return function (target: any, propertyKey: string | symbol, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;

    descriptor.value = function (...args: any[]) {
      console.log(`Executing ${String(propertyKey)} with arguments:`, args);
      return originalMethod.apply(this, args); // Execute original logic
    };
    return descriptor;
  };
}
```
**Usage in Components:**
```typescript
@LogMethod()
saveUserProfile(userId: number) {
  // Logic here
}
```

> 💡 **Interviewer Focus:** TypeScript meta-programming, modifying class descriptors, and using decorators to reuse cross-cutting logic.

</details>
<hr/>

### ❓ Q87. **What is the difference between Webpack and Esbuild compilers in Angular builds?**
<details>
<summary><b>👀 Show Answer</b></summary>

* **Webpack (Classic Compiler):** A feature-rich module bundler. It processes import trees sequentially, which can lead to slower compilation times in large projects.
* **Esbuild (Modern Compiler):** A Go-based compiler used by default in modern Angular (17+). It compiles code in parallel, yielding up to **10x faster build speeds** and faster hot-reloading during development.

> 💡 **Interviewer Focus:** Build optimizations, compilation speed improvements, and hot-reload latency.

</details>
<hr/>

### ❓ Q88. **Explain how to debug memory leaks in Angular components.**
<details>
<summary><b>👀 Show Answer</b></summary>

Memory leaks in Angular components are usually caused by active references that prevent the garbage collector from reclaiming the component's memory (such as active subscriptions, unclosed event listeners, or global timeouts).

#### 🛠️ Debugging Steps:
1. **Take Heap Snapshots:** Open Chrome DevTools, navigate to the **Memory** tab, and take a heap snapshot.
2. **Interact with the App:** Open and close the suspected component (e.g. navigate to a route and back) 5–10 times.
3. **Compare Snapshots:** Take a second heap snapshot and compare it to the first. Filter by the component's class name. If the component's constructor count remains greater than 0, it is leaking memory.
4. **Inspect Retainers:** Inspect the component's retainer tree in the snapshot to find what is holding active references to it (e.g. an active RxJS observable subscription).

> 💡 **Interviewer Focus:** Profiling heap snapshots, comparing active constructor allocations, and identifying common retainer sources.

</details>
<hr/>

### ❓ Q89. **What are route reuse strategies?**
<details>
<summary><b>👀 Show Answer</b></summary>

By default, Angular destroys the active component when navigating away from a route. If a user returns to that route, Angular creates a new instance of the component from scratch.

To preserve component state across navigations (e.g., to prevent destroying a dashboard view), implement a custom **`RouteReuseStrategy`**:

```typescript
import { RouteReuseStrategy, ActivatedRouteSnapshot, DetachedRouteHandle } from '@angular/router';

export class CustomRouteReuseStrategy implements RouteReuseStrategy {
  private handlers: { [key: string]: DetachedRouteHandle } = {};

  shouldDetach(route: ActivatedRouteSnapshot): boolean { return true; } // Cache this route
  store(route: ActivatedRouteSnapshot, handle: DetachedRouteHandle): void {
    this.handlers[route.routeConfig?.path || ''] = handle; // Save instance
  }
  shouldAttach(route: ActivatedRouteSnapshot): boolean {
    return !!this.handlers[route.routeConfig?.path || ''];
  }
  retrieve(route: ActivatedRouteSnapshot): DetachedRouteHandle | null {
    return this.handlers[route.routeConfig?.path || ''] || null;
  }
  shouldReuseRoute(future: ActivatedRouteSnapshot, curr: ActivatedRouteSnapshot): boolean {
    return future.routeConfig === curr.routeConfig;
  }
}
```

Register your custom strategy in `app.config.ts`:
```typescript
providers: [{ provide: RouteReuseStrategy, useClass: CustomRouteReuseStrategy }]
```

> 💡 **Interviewer Focus:** Caching components to preserve state across navigations, and implementing `RouteReuseStrategy` methods.

</details>
<hr/>

### ❓ Q90. **How do you implement offline synchronization patterns?**
<details>
<summary><b>👀 Show Answer</b></summary>

Implementing offline sync involves caching data locally when offline and syncing changes with the server when connectivity returns:

1. **Local Caching:** Use **IndexedDB** (via libraries like `Dexie.js`) to store payloads locally, as it supports larger datasets than `localStorage`.
2. **Detect Network Status:** Use the browser's `navigator.onLine` API or RxJS streams to track network connectivity status:
   ```typescript
   isOnline$ = merge(
     fromEvent(window, 'online').pipe(map(() => true)),
     fromEvent(window, 'offline').pipe(map(() => false))
   );
   ```
3. **Queue Requests:** If offline, save write requests (such as form submissions or updates) to an IndexedDB queue.
4. **Sync Queue:** When connectivity returns, read the queue, send requests sequentially to the server, and clear successful items from local storage.

> 💡 **Interviewer Focus:** Using IndexedDB for offline storage, monitoring network status, and synchronization conflict resolution.

</details>
<hr/>

### ❓ Q91. **What is the purpose of `NgZone` and how do you bypass it?**
<details>
<summary><b>👀 Show Answer</b></summary>

**`NgZone`** is a wrapper around `Zone.js` that triggers change detection across the entire application whenever an asynchronous task (such as a click, timer, or HTTP response) completes.

#### ⚙️ Bypassing NgZone:
High-frequency tasks (such as mouse move events, scroll animations, or Canvas updates) trigger change detection on every emission, which can slow down rendering. 

You can bypass this by running these tasks outside Angular's zone using **`runOutsideAngular`**:

```typescript
constructor(private zone: NgZone) {}

listenToScrollEvents() {
  this.zone.runOutsideAngular(() => {
    window.addEventListener('scroll', () => {
      this.animateElements(); // Runs without triggering change detection
    });
  });
}
```

If you need to update the UI once the task completes, re-enter Angular's zone using `run`:
```typescript
this.zone.run(() => { this.isAnimationDone = true; }); // Triggers change detection
```

> 💡 **Interviewer Focus:** Preventing unnecessary change detection runs, and using `runOutsideAngular` to optimize performance.

</details>
<hr/>

### ❓ Q92. **How do you configure custom control value accessors (`NG_VALUE_ACCESSOR`)?**
<details>
<summary><b>👀 Show Answer</b></summary>

To bind custom input components (such as a custom color picker or star rating component) to Reactive Forms, implement the **`ControlValueAccessor`** interface and register it with the `NG_VALUE_ACCESSOR` provider token:

```typescript
import { Component, forwardRef } from '@angular/core';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';

@Component({
  selector: 'app-star-rating',
  standalone: true,
  providers: [{
    provide: NG_VALUE_ACCESSOR,
    useExisting: forwardRef(() => StarRatingComponent),
    multi: true
  }],
  template: `<div (click)="rate(5)">★★★★★</div>`
})
export class StarRatingComponent implements ControlValueAccessor {
  rating = 0;
  onChange = (val: number) => {};
  onTouched = () => {};

  writeValue(value: number): void { this.rating = value; } // Sets value programmatically
  registerOnChange(fn: any): void { this.onChange = fn; } // Stores callback for updates
  registerOnTouched(fn: any): void { this.onTouched = fn; }
  
  rate(val: number) {
    this.rating = val;
    this.onChange(val); // Notifies form model
  }
}
```

> 💡 **Interviewer Focus:** Implementing `ControlValueAccessor` methods, multi-providers registration, and mapping custom components to Angular forms.

</details>
<hr/>

### ❓ Q93. **What is the difference between static and dynamic hydration?**
<details>
<summary><b>👀 Show Answer</b></summary>

* **Static Hydration (Standard):** Hydrates the entire page as soon as the client bundle loads, making all server-rendered elements interactive at once.
* **Dynamic (Progressive) Hydration:** Hydrates components on-demand based on client interactions or viewport visibility. For example, a heavy comments component is not hydrated until it enters the viewport, reducing initial JavaScript execution times.

> 💡 **Interviewer Focus:** Hydration timing optimizations and reducing main thread execution latency.

</details>
<hr/>

### ❓ Q94. **Explain how content security policies (CSP) are configured.**
<details>
<summary><b>👀 Show Answer</b></summary>

A **Content Security Policy (CSP)** is an HTTP response header that prevents cross-site scripting (XSS) and injection attacks by restricting the sources from which the browser can load scripts, styles, and other resources.

#### ⚙️ Configuration in Angular:
1. **Enable Trusted Types:** Configure CSP header policies to only allow trusted HTML wrappers:
   ```http
   Content-Security-Policy: require-trusted-types-for 'script';
   ```
2. **Apply nonces for Inline Styles:** Angular inserts styles into the document head at runtime. To allow these inline styles without disabling CSS source protection (`unsafe-inline`), configure a **nonce** attribute in your script tags:
   ```html
   <meta name="csp-nonce" content="random-unique-nonce-string">
   ```
   Angular reads this nonce and appends it to all generated `<style>` tags automatically.

> 💡 **Interviewer Focus:** Preventing script injection, using CSP headers, and configuring nonces.

</details>
<hr/>

### ❓ Q95. **How do you profile change detection cycles using Angular DevTools?**
<details>
<summary><b>👀 Show Answer</b></summary>

**Angular DevTools** is a browser extension used to profile change detection performance:

1. **Open the Profiler Tab:** Open Angular DevTools and click the **Profiler** tab.
2. **Record Interaction:** Click record and perform the slow interaction (like typing or scrolling).
3. **Analyze Flame Graph:** Review the generated flame graph. Each bar represents a change detection cycle. Taller bars indicate longer execution times.
4. **Identify Slow Components:** Click a component in the tree to view how long it took to check and what triggered the change detection run. This helps identify unnecessary checks, allowing you to optimize performance by switching components to `OnPush`.

> 💡 **Interviewer Focus:** Measuring rendering bottlenecks, using the Flame Graph, and identifying slow components.

</details>
<hr/>

### ❓ Q96. **What is the compile process under Ivy?**
<details>
<summary><b>👀 Show Answer</b></summary>

**Ivy** is Angular's compiler and rendering engine. Its compilation process is designed to be highly optimized and tree-shakable:

1. **AOT Compilation:** Compiles templates and TypeScript code into JavaScript before the browser downloads it, catching errors during the build process.
2. **Template Compilation:** Compiles HTML templates into direct, procedural JavaScript instructions (rather than large JSON metadata structures).
3. **Incremental Builds:** Only recompiles modified components and their direct dependencies, speeding up build times in large codebases.

> 💡 **Interviewer Focus:** Procedural templates compilation, tree-shakability, and incremental build optimizations.

</details>
<hr/>

### ❓ Q97. **Explain how to configure custom template outlets.**
<details>
<summary><b>👀 Show Answer</b></summary>

You can dynamically render templates and pass context objects to them using the **`NgTemplateOutlet`** directive:

```html
<!-- Child Component Template (list.component.html) -->
<ul>
  <li *ngFor="let item of items">
    <!-- Render custom template provided by parent, passing context -->
    <ng-container *ngTemplateOutlet="itemTemplate; context: { $implicit: item }"></ng-container>
  </li>
</ul>
```
**Parent Usage:**
```html
<app-list [items]="users" [itemTemplate]="customUserTemplate"></app-list>

<ng-template #customUserTemplate let-user>
  <div class="user-card">
    <h4>{{ user.name }}</h4>
  </div>
</ng-template>
```

> 💡 **Interviewer Focus:** Dynamically rendering templates, injecting context objects, and decoupling layouts from components.

</details>
<hr/>

### ❓ Q98. **How do you implement tree-shakability for custom components?**
<details>
<summary><b>👀 Show Answer</b></summary>

To make custom components tree-shakable:
1. **Declare them as Standalone:** Set `standalone: true` in the `@Component` decorator.
2. **Avoid Global Module Registrations:** Do not register components in shared module arrays.
3. **Use ES6 Imports:** Import the component only in the components or routes where it is actually used. If a component is never imported, the bundler can safely exclude it from the final production bundle.

> 💡 **Interviewer Focus:** Tree-shaking mechanisms, standalone components, and static import analysis.

</details>
<hr/>

### ❓ Q99. **What are web workers and how do you leverage them in Angular?**
<details>
<summary><b>👀 Show Answer</b></summary>

JavaScript is single-threaded. Running CPU-intensive tasks (like image processing or large calculations) on the main thread can cause the UI to freeze.

**Web Workers** allow you to run these calculations on a background thread:
1. **Generate Worker:** Create a worker file using the CLI:
   ```bash
   ng generate web-worker my-worker
   ```
2. **Offload Task:** In your component, instantiate the Web Worker and listen for messages. Send heavy tasks to the worker, and handle results once they are returned to the main thread:
   ```typescript
   const worker = new Worker(new URL('./my-worker.worker', import.meta.url));
   worker.postMessage({ data: heavyData }); // Send task to worker
   worker.onmessage = ({ data }) => {
     console.log('Result from worker:', data);
   };
   ```

> 💡 **Interviewer Focus:** Keeping the UI responsive, offloading tasks from the main thread, and Web Worker communication APIs.

</details>
<hr/>

### ❓ Q100. **Explain dynamic configuration loading before application boot.**
<details>
<summary><b>👀 Show Answer</b></summary>

To load configurations (such as API URLs or feature flags) before the application bootstraps:
1. Register a provider using the **`APP_INITIALIZER`** token.
2. Configure the provider to return a function that returns a **Promise**.
3. Angular delays application bootstrapping until this Promise resolves, ensuring configurations are loaded and available when the application starts.

```typescript
import { APP_INITIALIZER, inject } from '@angular/core';

export function initializeApp() {
  const configService = inject(ConfigService);
  return () => configService.loadConfig(); // Returns Promise
}

// Register in app.config.ts:
providers: [
  {
    provide: APP_INITIALIZER,
    useFactory: initializeApp,
    multi: true
  }
]
```

> 💡 **Interviewer Focus:** Bootstrapping lifecycles, using the `APP_INITIALIZER` token, and delaying startup until dynamic configurations are loaded.

</details>
<hr/>

### 🧭 Navigation

| ⬅️ Previous | 🏠 Index | ➡️ Next |
| :--- | :---: | ---: |
| [⬅️ React Native](./05_ReactNative.md) | [Home](./00_Index.md) | [➡️ Khelo Tech Prep](./khelo_tech.md) |
