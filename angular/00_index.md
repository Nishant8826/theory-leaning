# Angular Master Learning Repository

Welcome to the ultimate Angular learning roadmap. This repository is structured to guide you from an absolute beginner with zero Angular experience to a senior enterprise-level Angular architect. Every topic contains deep explanations, architecture impact, performance/scalability analysis, real-world examples, runnable code blocks, and common interview questions.

---

## 🗺️ Angular Learning Roadmap

### 📦 1. Foundation & Setup
* [01. Introduction to Angular](./01_Introduction_to_Angular.md) - History, comparison with other frameworks (React/Vue), SPA architecture, and ecosystem overview.
* [02. Setup and Environment](./02_Setup_and_Environment.md) - Node.js, npm, installing Angular CLI, and creating your first application.
* [03. TypeScript Fundamentals](./03_Typescript_Fundamentals.md) - Variables, interfaces, type aliases, enums, classes, OOP, generics, decorators, async/await, and promises.
* [04. Angular Architecture](./04_Angular_Architecture.md) - Bootstrapping flow, modularity, components vs services, and Standalone component architecture.

### 🧱 2. Core Angular & Directives
* [05. Components and Templates](./05_Components_and_Templates.md) - Component design, HTML templates, property/event binding, interpolation, two-way binding, and template reference variables.
* [06. Pipes](./06_Pipes.md) - Transform data in templates, built-in pipes, and writing custom pure/impure pipes.
* [07. Directives](./07_Directives.md) - Attribute, structural, and custom directives. Detailed usage of `@HostBinding` and `@HostListener`.
* [08. Component Lifecycle](./08_Component_Lifecycle.md) - Hook execution phase and order (OnInit, OnChanges, DoCheck, AfterViewInit, OnDestroy).
* [09. Component Communication](./09_Component_Communication.md) - Parent-child data flow, `@Input`, `@Output`, `EventEmitter`, `@ViewChild`, `@ContentChild`, `@ViewChildren`, content projection, and dynamic component loading.

### ⚡ 3. Modern Signals Architecture
* [10. Signals](./10_Signals.md) - Reactivity reinvented. Writable Signals, computed values, effects, signal inputs, and Signals vs RxJS architecture.

### 💉 4. Dependency Injection & Services
* [11. Dependency Injection](./11_Dependency_Injection.md) - Injector trees, providers (useClass, useValue, useFactory, useExisting), hierarchical injection, multi-providers, and injection tokens.
* [12. Services and Business Logic](./12_Services_and_Business_Logic.md) - Singleton services, shared services, and partitioning business logic from presentation.

### 🧭 5. Routing & Navigation
* [13. Routing and Navigation](./13_Routing_and_Navigation.md) - Configuration, Router Outlet, route/query parameters, child routes, lazy loading, resolvers, route guards (CanActivate, CanMatch), and custom route matchers.

### 📝 6. Forms
* [14. Template-Driven Forms](./14_Template_Driven_Forms.md) - Form state tracking, `ngModel`, and custom template validation.
* [15. Reactive Forms](./15_Reactive_Forms.md) - Programmatic forms, `FormControl`, `FormGroup`, `FormArray`, built-in validators, custom validation, async validators, and dynamic form builders.

### 🌐 7. HTTP Client & RxJS
* [16. HttpClient and API Integration](./16_HttpClient_and_API_Integration.md) - REST API interactions, interceptors (functional & class-based), error handling, retry policies, and auth flows.
* [17. RxJS Reactive Programming](./17_RxJS_Reactive_Programming.md) - Observables, Observers, Subscriptions, Subjects (Subject, BehaviorSubject, ReplaySubject), and comprehensive operators guide.

### 💾 8. State Management
* [18. State Management](./18_State_Management.md) - Component state, Service-based state, Signal-based state, NgRx Store (Actions, Reducers, Effects, Selectors, Entity), and NgRx Signal Store.

### 🛡️ 9. Security & Authentication
* [19. Authentication and Authorization](./19_Authentication_and_Authorization.md) - JWT flow, access/refresh tokens, role-based access control, secure local/session storage.
* [20. Angular Material](./20_Angular_Material.md) - UI design system, configuration, theming, table, dialog, and standard layouts.
* [21. Performance Optimization](./21_Performance_Optimization.md) - Change detection optimization (OnPush), Zoneless Angular, lazy/deferred loading (`@defer`), trackBy, virtual scrolling, tree-shaking, and bundle size reduction.

### 🧪 10. Advanced Concepts, Testing, & SSR
* [22. Testing (Jasmine & Jest)](./22_Testing_Jasmine_Jest.md) - Unit testing components/services, testbeds, integration tests, E2E testing (Playwright/Cypress).
* [23. Security Best Practices](./23_Security_Best_Practices.md) - Sanitization, DomSanitizer, XSS, CSRF protection, and CSP headers.
* [24. SSR and Advanced Concepts](./24_SSR_and_Advanced_Concepts.md) - Server-Side Rendering (SSR), Angular Universal, Hydration, SEO, PWAs, Micro-frontends (Module Federation), and Monorepos (Nx).
* [25. Enterprise Architecture](./25_Enterprise_Architecture.md) - Domain-Driven Design (DDD), feature folders, Smart/Dumb component separation, Core vs Shared layers, state/UI boundaries.
* [26. Deployment and CI/CD](./26_Deployment_and_CI_CD.md) - Environment files, Dockerization, Nginx routing configs, and CI/CD pipelines (GitHub Actions, AWS, Azure, Firebase).
* [27. Real World E-Commerce Project](./27_Real_World_ECommerce_Project.md) - Architecture, routes, state, folder hierarchy, and authentication flow for an enterprise-level shop application.

### 🎯 11. Interview Preparation
* [28. Beginner Interview Prep](./28_Interview_Prep_Beginner.md) - Elementary core concepts, installation, TypeScript, and template syntax.
* [29. Interview Prep - Intermediate](./29_Interview_Prep_Intermediate.md) - Forms, Services, Routing, Directives, Pipes, and basic RxJS.
* [30. Interview Prep - Advanced](./30_Interview_Prep_Advanced.md) - Performance, custom DI, complex RxJS operators, state management, and SSR.
* [31. Scenario and System Design](./31_Interview_Prep_Scenario_and_System_Design.md) - Real-world architectural scenario answers, optimization problems, and high-level Angular system design.

---

# Angular Quick Revision Notes

Use these notes to refresh your entire Angular knowledge in under 30 minutes. Click any topic heading to navigate directly to its detailed file.

---

## [01. Introduction to Angular](./01_Introduction_to_Angular.md)
* **Purpose**: Foundational overview of Angular, SPA architectures, and how it compares to React/Vue.
* **Key Points**:
  - Opinionated framework built with TypeScript and developed by Google.
  - Loads a single index page and dynamically updates DOM parts using JavaScript.
  - Bypasses legacy modules using standalone components and bootstrap configurations.
* **Remember**: Angular provides a complete set of features out-of-the-box, enforcing strict structures across teams.

## [02. Setup and Environment](./02_Setup_and_Environment.md)
* **Purpose**: Setting up Node.js runtime, npm registry, and installing the Angular CLI.
* **Key Points**:
  - The CLI manages code generation, development servers, production builds, and unit testing.
  - Local configurations are locked in `package.json` and executed via npm scripts for CI/CD consistency.
* **Remember**: Use `nvm` to manage Node versions and use `npx ng` to prevent global CLI version conflicts.

## [03. TypeScript Fundamentals](./03_Typescript_Fundamentals.md)
* **Purpose**: Adding compile-time type safety, interfaces, enums, generics, and async handling to JavaScript.
* **Key Points**:
  - Type narrowing (using `typeof`/`instanceof`) is required when managing dynamic `unknown` types.
  - Generics enforce type reuse across repositories, classes, and services.
  - TypeScript annotations are completely stripped away during build compilation (zero runtime overhead).
* **Remember**: Avoid using `any` as it disables type checks; prefer literal unions or `unknown` structures instead.

## [04. Angular Architecture](./04_Angular_Architecture.md)
* **Purpose**: Architectural structure of Angular applications, bootstrap phases, and standalone setups.
* **Key Points**:
  - Single application entry point `main.ts` calls `bootstrapApplication()` with configuration values.
  - Decoupled architecture where templates present views and services coordinate business logic.
  - DI injectors instantiate and supply classes to component instances dynamically.
* **Remember**: Standalone architecture is the default standard in modern Angular, bypassing `NgModule`.

## [05. Components and Templates](./05_Components_and_Templates.md)
* **Purpose**: Creating UI view blocks using component logic, templates, CSS styles, and bindings.
* **Key Points**:
  - Interpolation (`{{ }}`) and Property Bindings (`[src]`) pass state values down to template views.
  - Event Bindings (`(click)`) pass events up to run methods in component classes.
  - Template Reference Variables (`#ref`) grant direct template access to DOM element values.
* **Remember**: Keep templates declarative and avoid running expensive helper methods in bindings.

## [06. Pipes](./06_Pipes.md)
* **Purpose**: Transform raw data values for display directly inside templates.
* **Key Points**:
  - Built-in pipes handle common formats like currencies, dates, cases, and JSON values.
  - Pure pipes cache outputs, only executing when input primitive values or references change.
  - The `Async` pipe automatically manages observable subscriptions, preventing memory leaks.
* **Remember**: Avoid mutating array elements directly when using pure pipes; swap the reference array instead.

## [07. Directives](./07_Directives.md)
* **Purpose**: Attach behaviors, styles, or DOM modifications to templates.
* **Key Points**:
  - Attribute directives change element styling, while structural directives modify the DOM tree.
  - Custom directives use `@HostBinding` to modify host attributes and `@HostListener` to track host events.
* **Remember**: Always use Renderer2 or Host decorators instead of raw nativeElement mutations to support SSR.

## [08. Component Lifecycle](./08_Component_Lifecycle.md)
* **Purpose**: Intercepting key phases of component execution from initialization to destruction.
* **Key Points**:
  - `ngOnChanges` executes when inputs update, while `ngOnInit` handles initial data fetches.
  - `ngAfterViewInit` is the first hook where component DOM queries are fully accessible.
  - `ngOnDestroy` runs cleanup tasks, closing active connections and subscriptions.
* **Remember**: Do not execute network requests inside constructors; always delegate them to `ngOnInit`.

## [09. Component Communication](./09_Component_Communication.md)
* **Purpose**: Sharing data, events, and layouts across nested component structures.
* **Key Points**:
  - Unidirectional data flow: inputs (`@Input`) send data down; outputs (`@Output`) emit events up.
  - View queries (`@ViewChild`) allow components to interact with local template children.
  - Content projection (`<ng-content>`) allows parent templates to inject custom layouts.
* **Remember**: Query projected children using `@ContentChild` instead of `@ViewChild` inside templates.

## [10. Signals](./10_Signals.md)
* **Purpose**: Fine-grained reactivity that tracks state reads and triggers targeted UI updates.
* **Key Points**:
  - Writable Signals track local state changes, computed signals derive cached values, and effects run side-effects.
  - Allows components to execute without Zone.js triggers (Zoneless architecture).
  - Exposes modern inputs using the `input()` function API.
* **Remember**: Always invoke signals as function calls `{{ name() }}` in templates.

## [11. Dependency Injection](./11_Dependency_Injection.md)
* **Purpose**: Decoupling classes from their dependencies by managing class resolution centrally.
* **Key Points**:
  - Resolves dependencies by traversing up the hierarchical injector tree.
  - Supports custom class mapping (`useClass`), values (`useValue`), and factory logic (`useFactory`).
  - Injection Tokens identify non-class values like configuration parameters.
* **Remember**: Use the modern `inject()` function to write cleaner classes and simplify inheritance.

## [12. Services and Business Logic](./12_Services_and_Business_Logic.md)
* **Purpose**: Encapsulating non-UI logic, computations, and API configurations.
* **Key Points**:
  - `@Injectable({ providedIn: 'root' })` registers services as tree-shakable global singletons.
  - Keeps component views thin and logic architectures clean and testable.
* **Remember**: Expose state properties as read-only computed signals or observables.

## [13. Routing and Navigation](./13_Routing_and_Navigation.md)
* **Purpose**: Mapping browser URLs to component views without reloading pages.
* **Key Points**:
  - Configuration array routes URL paths to static or lazy-loaded components.
  - Functional guards check permissions and block unauthorized access.
  - Dynamic parameters and query configurations pass state values through navigation.
* **Remember**: Lazy load route views using `loadComponent` to optimize bundle sizes.

## [14. Template-Driven Forms](./14_Template_Driven_Forms.md)
* **Purpose**: Creating and managing forms using HTML directive bindings.
* **Key Points**:
  - Automatically builds form models behind the scenes using `ngModel` and the parent form directive.
  - Uses standard HTML attributes (like `required`) to handle simple validation rules.
* **Remember**: Always set the `name` attribute on input tags when using `ngModel`.

## [15. Reactive Forms](./15_Reactive_Forms.md)
* **Purpose**: Building model-driven forms that offer predictable state and type-safe validation.
* **Key Points**:
  - Programmatically declared using `FormControl`, `FormGroup`, and `FormArray`.
  - Values and validation statuses flow through RxJS streams.
  - Supports async validators to verify fields against database APIs in real-time.
* **Remember**: Use `updateOn: 'blur'` to prevent async validators from triggering on every keystroke.

## [16. HttpClient and API Integration](./16_HttpClient_and_API_Integration.md)
* **Purpose**: Communicating with remote REST APIs over HTTP.
* **Key Points**:
  - Returns cold observables, meaning requests only send when subscribed to.
  - Functional interceptors append authorization headers and handle token refresh flows globally.
  - Supports automatic JSON parsing and type-safe response casting.
* **Remember**: Clean up subscriptions in interceptors or handle retry strategies carefully.

## [17. RxJS Reactive Programming](./17_RxJS_Reactive_Programming.md)
* **Purpose**: Coordinating complex asynchronous events as continuous data streams.
* **Key Points**:
  - Observables emit values over time, while subscriptions handle stream executions.
  - BehaviorSubjects store and replay their latest value to new subscribers immediately.
  - Flattening operators (`switchMap`, `mergeMap`, `concatMap`, `exhaustMap`) handle nested streams.
* **Remember**: Use `switchMap` to cancel active search requests when new values emit.

## [18. State Management](./18_State_Management.md)
* **Purpose**: Maintaining a single source of truth for application state.
* **Key Points**:
  - State changes are dispatched via actions, processed by reducers, and queried via selectors.
  - Light state is managed using shared services and signals, while large apps use global stores.
  - NgRx Signal Store provides a functional state management API built on Signals.
* **Remember**: Keep state objects immutable, updating them using spread operators.

## [19. Authentication and Authorization](./19_Authentication_and_Authorization.md)
* **Purpose**: Verifying user identities and managing access permissions.
* **Key Points**:
  - Short-lived Access Tokens authorize requests, and Refresh Tokens request new access tokens.
  - Interceptors append JWT headers, and route guards block unauthorized navigation.
* **Remember**: Use `CanMatch` functional guards to block lazy-loaded modules from downloading.

## [20. Angular Material](./20_Angular_Material.md)
* **Purpose**: Access to pre-built Material Design UI controls.
* **Key Points**:
  - Implements components like data tables, dialogues, and form fields.
  - Customize colors and layouts using SASS variables and theme configs.
  - Accessibility behaviors are managed internally by the Angular CDK overlay engine.
* **Remember**: Use official SCSS mixins instead of custom styles to avoid breaking upgrades.

## [21. Performance Optimization](./21_Performance_Optimization.md)
* **Purpose**: Optimizing application load times and change detection checks.
* **Key Points**:
  - OnPush change detection strategy skips components unless inputs change.
  - Lazy load components when they enter the viewport using `@defer` blocks.
  - Track list loops using unique identifiers to avoid rendering list items again.
* **Remember**: Keep change detection checks low to support Zoneless setups.

## [22. Testing (Jasmine & Jest)](./22_Testing_Jasmine_Jest.md)
* **Purpose**: Writing unit, integration, and E2E tests to verify behavior.
* **Key Points**:
  - `TestBed` initializes dynamic modules to test components and services in isolation.
  - Query elements and trigger change detection using component fixtures.
  - E2E tools (like Playwright and Cypress) run user scenarios in real browsers.
* **Remember**: Verify that no open network calls remain using `HttpTestingController.verify()`.

## [23. Security Best Practices](./23_Security_Best_Practices.md)
* **Purpose**: Securing applications against vulnerabilities like XSS and CSRF.
* **Key Points**:
  - Angular sanitizes all template inputs by default, stripping out malicious tags.
  - `DomSanitizer` can bypass sanitization when explicitly rendering trusted content.
  - Cookie credentials protect API communication using CSRF header checks.
* **Remember**: Never pass raw user inputs directly into `bypassSecurityTrustHtml`.

## [24. SSR and Advanced Concepts](./24_SSR_and_Advanced_Concepts.md)
* **Purpose**: Pre-rendering HTML templates on Node servers to improve SEO and load times.
* **Key Points**:
  - Static HTML is generated on the server and hydrated on the client.
  - Safe execution requires platform checks before accessing browser-only APIs.
  - Large workspaces can be managed using Nx monorepo patterns.
* **Remember**: Wrap references to browser globals in `isPlatformBrowser` checks.

## [25. Enterprise Architecture](./25_Enterprise_Architecture.md)
* **Purpose**: Structuring large codebases using clean layer configurations.
* **Key Points**:
  - Domain-Driven Design groups related features, services, and state by domain folders.
  - Smart components manage state and APIs, while Dumb components handle UI presentation.
  - Decoupling logic keeps features isolated and easy to test.
* **Remember**: Do not inject services or store configurations directly into Dumb components.

## [26. Deployment and CI/CD](./26_Deployment_and_CI_CD.md)
* **Purpose**: Packaging, hosting, and deploying production code.
* **Key Points**:
  - Production builds apply deep tree-shaking to minimize bundle sizes.
  - Docker configures container setups, and Nginx handles routing fallbacks.
  - GitHub Actions automate builds, tests, and deployments to cloud hosts.
* **Remember**: Always configure Nginx's `try_files` rule to support client-side routing.

## [27. Real World E-Commerce Project](./27_Real_World_ECommerce_Project.md)
* **Purpose**: Structuring real-world routing, state, and API integrations in a shop app.
* **Key Points**:
  - Domain boundaries partition shopping cart, catalog, and checkout features.
  - Features are lazy-loaded on-demand and secured using authentication guards.
  - Global shopping cart state is managed using the `NgRx Signal Store`.
* **Remember**: Cache API requests to minimize redundant network calls.

## [28. Beginner Interview Prep](./28_Interview_Prep_Beginner.md)
* **Purpose**: Key topics and questions for entry-level developers.
* **Key Points**:
  - Covers Angular CLI commands, data bindings, and interpolation.
  - Explains the difference between components and directives.
  - Validates basic TypeScript syntax and standalone component structures.
* **Remember**: Practice standard CLI commands and simple binding setups.

## [29. Interview Prep - Intermediate](./29_Interview_Prep_Intermediate.md)
* **Purpose**: Intermediate questions on form validation and lifecycle hooks.
* **Key Points**:
  - Explains the differences between reactive and template-driven forms.
  - Explains lifecycle hooks, custom directives, and pure/impure pipes.
  - Focuses on basic RxJS stream management and subscription cleanups.
* **Remember**: Review component lifecycle hooks and reactive form validations.

## [30. Interview Prep - Advanced](./30_Interview_Prep_Advanced.md)
* **Purpose**: Advanced questions on optimization and rendering architectures.
* **Key Points**:
  - Focuses on OnPush change detection, Zoneless setups, and SSR.
  - Validates custom DI provider declarations and multi-providers.
  - Focuses on RxJS flattening operators and silent token refresh interceptors.
* **Remember**: Practice debugging hydration errors and change detection checks.

## [31. Scenario and System Design](./31_Interview_Prep_Scenario_and_System_Design.md)
* **Purpose**: Senior engineering scenario questions and system designs.
* **Key Points**:
  - Covers designing real-time dashboards and multi-tenant portals.
  - Focuses on caching strategies, monorepo systems, and state models.
  - Focuses on preventing layout shifts and optimizing page load speeds.
* **Remember**: Practice modeling domain architectures and caching structures.

