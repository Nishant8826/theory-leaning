# Component Lifecycle

## What is it?
The Component Lifecycle represents the series of phases a component passes through from its initial instantiation to its final destruction. Angular provides "lifecycle hooks"—interfaces that allow us to intercept these phases and run custom logic during those transitions.

## Why do we need it?
A component needs to perform setup tasks (like fetching API data) and cleanup tasks (like cancelling timers or unsubscribing from active event streams). Without lifecycle hooks, developers wouldn't know when a component's inputs are ready, when its children are rendered, or when it is about to be removed from the DOM, leading to errors and memory leaks.

```
Lifecycle Hook Execution Order:
Constructor ──> ngOnChanges ──> ngOnInit ──> ngDoCheck
                 ──> ngAfterContentInit ──> ngAfterContentChecked
                 ──> ngAfterViewInit ──> ngAfterViewChecked ──> ngOnDestroy
```

## How does it work?
Angular manages the lifecycle internally. As it traverses the component tree, it executes specific hook methods if they are implemented on the component class:
1. **`constructor()`**: Native ES6 initialization. Dependency Injection resolution occurs here. No DOM updates or input properties are available yet.
2. **`ngOnChanges()`**: Triggered when any input bindings (`@Input` / `input()`) change.
3. **`ngOnInit()`**: Runs once after inputs are bound. Recommended place to fetch data.
4. **`ngAfterViewInit()`**: Executes after the component's view and child views are rendered.
5. **`ngOnDestroy()`**: Runs right before the component is destroyed. Essential for cleanup.

## Impact
* **Application Architecture**: Directs where data loading, DOM queries, and resource cleanups take place.
* **Performance**: Proper use of hooks prevents memory leaks, slow loading, and layout shifts.
* **Maintainability**: Keeps initialization logic isolated from teardown and event logic.

## Real World Example
In a stock trading widget, `ngOnInit` starts a WebSocket connection to fetch stock prices, `ngOnChanges` updates the chart when a new stock symbol is selected, and `ngOnDestroy` closes the WebSocket connection when the user leaves the page.

## Syntax
To implement a lifecycle hook, import the interface and implement its corresponding method:
```typescript
import { Component, OnInit, OnDestroy } from '@angular/core';

@Component({ ... })
export class MyComponent implements OnInit, OnDestroy {
  ngOnInit(): void {
    // Component initialization logic
  }

  ngOnDestroy(): void {
    // Clean up logic
  }
}
```

## Code Examples
A comprehensive component demonstrating the execution sequence of lifecycle hooks:

```typescript
import { 
  Component, 
  Input, 
  OnInit, 
  OnChanges, 
  DoCheck, 
  AfterViewInit, 
  OnDestroy, 
  SimpleChanges 
} from '@angular/core';

@Component({
  selector: 'app-lifecycle-logger',
  standalone: true,
  template: `
    <div class="log-card">
      <h4>Lifecycle Monitor</h4>
      <p>Active User: {{ user }}</p>
    </div>
  `,
  styles: [`
    .log-card { border: 1px solid #6366f1; padding: 12px; border-radius: 6px; }
  `]
})
export class LifecycleLoggerComponent implements OnInit, OnChanges, DoCheck, AfterViewInit, OnDestroy {
  @Input() user: string = '';

  constructor() {
    console.log('1. constructor - DI resolved, Inputs NOT ready yet');
  }

  ngOnChanges(changes: SimpleChanges): void {
    console.log('2. ngOnChanges - Inputs bound or modified:', changes);
  }

  ngOnInit(): void {
    console.log('3. ngOnInit - Initialization complete, fetching data for:', this.user);
  }

  ngDoCheck(): void {
    console.log('4. ngDoCheck - Change detection cycle triggered');
  }

  ngAfterViewInit(): void {
    console.log('5. ngAfterViewInit - DOM rendered, view templates accessible');
  }

  ngOnDestroy(): void {
    console.log('6. ngOnDestroy - Cleaning up references and timers');
  }
}
```

## Best Practices
1. **Never Make HTTP Requests in the Constructor**: Delegate API fetches to `ngOnInit` to ensure input properties are fully set.
2. **Always Unsubscribe in `ngOnDestroy`**: Clean up WebSocket streams, RxJS subscriptions (unless using `Async` pipe), timers, and global listeners in `ngOnDestroy`.
3. **Keep `ngDoCheck` Thin**: `ngDoCheck` runs on every change detection cycle. Putting heavy computations here will slow down the application.

## Common Mistakes
* **Querying children before ViewInit**: Querying element references via `@ViewChild` inside `ngOnInit` will return `undefined`. These elements are only available after `ngAfterViewInit` runs.
* **Modifying input data inside ngOnChanges**: Mutating incoming input bindings directly in `ngOnChanges`, which can lead to values changing unexpectedly and trigger the `ExpressionChangedAfterItHasBeenCheckedError`.

## Interview Questions & Answers
### Q: What is the purpose of `ngOnChanges` and when is it called?
**A**: `ngOnChanges` is executed before `ngOnInit` and whenever Angular detects a change to any component input binding (`@Input`). It receives a `SimpleChanges` object mapping input property names to their current and previous values, which is useful for responding to dynamic value changes.

### Q: Why shouldn't you write data fetching logic inside the component constructor?
**A**: The constructor is a feature of the ES6 class itself, not Angular. When the constructor runs, Angular hasn't initialized the component's input properties or bound data, meaning any inputs needed for the fetch will be `undefined`. `ngOnInit` is the correct hook because it runs after input bindings are ready.

## Summary
Lifecycle hooks intercept various stages of component execution. Use `ngOnChanges` to react to input updates, `ngOnInit` for data initialization, `ngAfterViewInit` for template DOM operations, and `ngOnDestroy` to clean up resources.

---

Previous : [Directives](./07_Directives.md) | Index : [Home](./00_index.md) | Next : [Component Communication](./09_Component_Communication.md)
