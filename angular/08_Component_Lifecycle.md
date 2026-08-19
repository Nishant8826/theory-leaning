# Component Lifecycle

## What is it?
The Component Lifecycle represents the sequential phases through which an Angular component travels, from its initial instantiation (creation) to its final destruction (removal from the DOM). Angular provides "Lifecycle Hooks" (TypeScript interfaces and methods) that allow developers to intercept these stages and execute custom logic at precise moments.

## Why do we need it?
Components frequently require setup tasks (such as fetching data from a backend API or establishing WebSocket channels) and teardown tasks (such as cancelling active timers, unsubscribing from RxJS streams, or disconnecting observers). 

Without lifecycle hooks, developers would not know when component inputs are ready, when child elements have finished rendering in the DOM, or when a component is about to be destroyed—leading to null pointer errors, UI rendering glitches, and severe memory leaks.

```
Lifecycle Hook Execution Sequence:
Constructor ──> ngOnChanges ──> ngOnInit ──> ngDoCheck
                 ──> ngAfterContentInit ──> ngAfterContentChecked
                 ──> ngAfterViewInit ──> ngAfterViewChecked ──> ngOnDestroy
```

## How does it work?
Angular manages the lifecycle internally. As it traverses the component tree, it invokes specific lifecycle hook methods if they are implemented on the component class:

1. **`constructor()`**: The standard ES6 class constructor. Used strictly for Dependency Injection (DI) parameter resolution. Component inputs and the DOM are not yet available at this stage.
2. **`ngOnChanges()`**: Executes before `ngOnInit()` and whenever one or more data-bound input properties (`@Input()` or signal inputs) change reference or value.
3. **`ngOnInit()`**: Executes once after Angular has initialized all component inputs. This is the optimal place to initiate HTTP calls and initialize component state.
4. **`ngDoCheck()`**: Executes immediately after `ngOnChanges()` and `ngOnInit()` during every change detection run. Used to detect and act upon changes that Angular's default change detection mechanism cannot detect automatically.
5. **`ngAfterContentInit()`**: Executes once after Angular projects external content (via `<ng-content>`) into the component view.
6. **`ngAfterContentChecked()`**: Executes after Angular checks the content projected into the component.
7. **`ngAfterViewInit()`**: Executes once after the component's view template and all child component views have been fully initialized and rendered in the DOM. This is the earliest point where `@ViewChild` DOM elements can be safely manipulated.
8. **`ngAfterViewChecked()`**: Executes after Angular finishes checking the component's view and child views for changes.
9. **`ngOnDestroy()`**: Executes immediately before Angular destroys the component and removes its view from the DOM. Essential for cleanup (unsubscribing from Observables, clearing `setInterval` timers, detaching event listeners).

## Impact
* **Application Architecture**: Ensures setup, data loading, DOM interactions, and teardown tasks occur at their designated, reliable stages.
* **Performance**: Proper use of teardown hooks eliminates browser memory leaks and prevents phantom event executions in the background.
* **Maintainability**: Organizes component initialization and teardown logic into clean, predictable segments.

## Real World Example
In a real-time cryptocurrency dashboard:
- `ngOnInit` initializes the WebSocket connection to stream live market ticker data.
- `ngOnChanges` updates the chart canvas whenever the user selects a different trading pair.
- `ngOnDestroy` cleanly terminates the WebSocket connection and clears background chart refresh intervals when the user navigates away.

## Syntax
To implement lifecycle hooks, import the corresponding interface and implement the method:

```typescript
import { Component, OnInit, OnDestroy } from '@angular/core';

@Component({
  selector: 'app-demo',
  standalone: true,
  template: `<p>Lifecycle Demo</p>`
})
export class MyComponent implements OnInit, OnDestroy {
  ngOnInit(): void {
    // Initialization and API calls
  }

  ngOnDestroy(): void {
    // Cleanup and unsubscribe
  }
}
```

## Code Examples
Below is a comprehensive logger component demonstrating the complete lifecycle execution order:

```typescript
import { 
  Component, 
  Input, 
  OnInit, 
  OnChanges, 
  DoCheck, 
  AfterContentInit,
  AfterContentChecked,
  AfterViewInit, 
  AfterViewChecked, 
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
      <ng-content></ng-content>
    </div>
  `,
  styles: [`
    .log-card { 
      border: 1px solid #6366f1; 
      padding: 14px; 
      border-radius: 6px; 
      max-width: 400px;
    }
  `]
})
export class LifecycleLoggerComponent implements 
  OnChanges, 
  OnInit, 
  DoCheck, 
  AfterContentInit, 
  AfterContentChecked, 
  AfterViewInit, 
  AfterViewChecked, 
  OnDestroy 
{
  @Input() user: string = '';

  constructor() {
    console.log('1. constructor: DI resolved. Inputs and DOM are NOT ready yet.');
  }

  ngOnChanges(changes: SimpleChanges): void {
    console.log('2. ngOnChanges: Input property changed or bound:', changes);
  }

  ngOnInit(): void {
    console.log('3. ngOnInit: Initialization complete. Fetching data for user:', this.user);
  }

  ngDoCheck(): void {
    console.log('4. ngDoCheck: Custom change detection check executed.');
  }

  ngAfterContentInit(): void {
    console.log('5. ngAfterContentInit: Projected content (<ng-content>) initialized.');
  }

  ngAfterContentChecked(): void {
    console.log('6. ngAfterContentChecked: Projected content verified by change detector.');
  }

  ngAfterViewInit(): void {
    console.log('7. ngAfterViewInit: DOM rendered. View templates and child components are accessible.');
  }

  ngAfterViewChecked(): void {
    console.log('8. ngAfterViewChecked: View templates and child components verified.');
  }

  ngOnDestroy(): void {
    console.log('9. ngOnDestroy: Teardown triggered. Cleaning up timers, listeners, and subscriptions.');
  }
}
```

## Best Practices
1. **Never Make HTTP Requests in the Constructor**: Always use `ngOnInit` for data fetching. The constructor should only be used for lightweight Dependency Injection.
2. **Always Unsubscribe in `ngOnDestroy`**: To avoid memory leaks, manually unsubscribe from any RxJS Observables (if not using the `Async` pipe or `takeUntilDestroyed()`) and clear all active `setInterval`/`setTimeout` timers.
3. **Keep `ngDoCheck` Extremely Lightweight**: Because `ngDoCheck` executes on every single change detection cycle across the entire application, heavy loops or calculations inside it will degrade UI responsiveness.

## Common Mistakes
* **Querying ViewChildren in `ngOnInit`**: Attempting to access `@ViewChild` element references during `ngOnInit` returns `undefined` because template DOM rendering completes later in `ngAfterViewInit`.
* **Mutating Input Properties in `ngOnChanges`**: Mutating properties directly inside `ngOnChanges` can trigger infinite loops or cause the notorious `ExpressionChangedAfterItHasBeenCheckedError`.

## Interview Questions & Answers
### Q: What is the purpose of `ngOnChanges` and when is it called?
**A**: `ngOnChanges` is called before `ngOnInit` and whenever any data-bound `@Input()` property changes. It receives a `SimpleChanges` object containing the `currentValue`, `previousValue`, and a `isFirstChange()` helper for each changed input property.

### Q: Why should data-fetching logic be placed in `ngOnInit` instead of the constructor?
**A**: The constructor is a native ES6 class feature intended solely for instantiation and Dependency Injection. At the constructor stage, Angular has not yet evaluated or bound `@Input()` properties. Placing data fetching in `ngOnInit` guarantees all inputs and component configurations are fully initialized.

## Summary
Lifecycle hooks give developers precise control over every stage of a component's existence. Use `ngOnChanges` for responding to input changes, `ngOnInit` for initial data fetching, `ngAfterViewInit` for direct DOM queries, and `ngOnDestroy` for resource cleanup and memory leak prevention.

---

Previous : [Directives](./07_Directives.md) | Index : [Home](./00_index.md) | Next : [Component Communication](./09_Component_Communication.md)
